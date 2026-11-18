#!/usr/bin/env bash
# Prints counts for the slop audit. Run from the repo root.
#
# Usage: probe.sh [path ...]          default: every tracked source file
# Env:   NUANCE       extra ERE of APIs that need judgment, joined with |
#        CORRECTIONS  a TSV correction log; column 2 is the tag
#        DAYS         window for churn and reverts (default 90)
set -u
export LC_ALL=C

paths=("$@")
[ ${#paths[@]} -eq 0 ] && paths=(.)
days="${DAYS:-90}"

exts=':(glob)**/*.ts :(glob)**/*.tsx :(glob)**/*.js :(glob)**/*.jsx :(glob)**/*.mjs :(glob)**/*.py :(glob)**/*.go :(glob)**/*.rb :(glob)**/*.rs :(glob)**/*.kt :(glob)**/*.swift'
skip=':!:**/node_modules/** :!:**/dist/** :!:**/build/** :!:**/*.generated.* :!:**/*.d.ts :!:**/*.min.*'
tests=':!:**/*.test.* :!:**/*.spec.* :!:**/test/** :!:**/tests/** :!:**/__tests__/** :!:**/__mocks__/** :!:**/*.stories.* :!:**/*_test.*'

# shellcheck disable=SC2206
ALL=(-- ${paths[@]/#/:(top)} )
SRC=()
for p in "${paths[@]}"; do
  for e in $exts; do SRC+=("${e/\*\*/${p%/}/**}"); done
done
# shellcheck disable=SC2206
PROD=(-- "${SRC[@]}" $skip $tests)
# shellcheck disable=SC2206
ANY=(-- "${SRC[@]}" $skip)

P() { git grep -E "$@" "${PROD[@]}" 2>/dev/null; }
A() { git grep -E "$@" "${ANY[@]}" 2>/dev/null; }
sum() { awk -F: '{s+=$NF} END{print s+0}'; }
top() { sort -t: -k2 -rn | head -5 | sed 's/^/  /'; }
row() { printf '%-22s %s\n' "$1" "$2"; }

echo "## Size"
row "prod files" "$(git ls-files "${PROD[@]:1}" | wc -l | tr -d ' ')"
row "prod lines" "$(P -c '' | sum)"
row "prod comment lines" "$(P -c '^[[:space:]]*(//|/\*|\*|#)' | sum)"

echo; echo "## Nuance APIs (prod)"
nuance='useEffect|useLayoutEffect|useRef|setTimeout|setInterval|requestAnimationFrame|queueMicrotask'
[ -n "${NUANCE:-}" ] && nuance="$nuance|$NUANCE"
IFS='|' read -r -a apis <<< "$nuance"
for api in "${apis[@]}"; do
  n=$(P -c "(^|[^A-Za-z0-9_.])$api[<(]" | sum)
  [ "$n" -gt 0 ] && row "$api" "$n"
done
echo "hotspots:"
P -c "(^|[^A-Za-z0-9_.])($nuance)[<(]" | top

echo; echo "## Escape hatches (all source)"
for h in 'eslint-disable' 'biome-ignore' '@ts-ignore' '@ts-expect-error' 'as unknown as' 'as any' 'noqa' 'type: ignore' 'nolint' 'rubocop:disable' '#[allow(' 'unsafe '; do
  n=$(A -F -c -e "$h" | sum)
  [ "$n" -gt 0 ] && row "$h" "$n"
done
echo "by rule:"
A -h -o -E '(eslint-disable(-next-line|-line)?|biome-ignore[a-z-]*|noqa|nolint|rubocop:disable)[: ]+[A-Za-z0-9/@_-]+' \
  | sed -E 's/[[:space:]]+/ /' | sort | uniq -c | sort -rn | head -10 | sed 's/^/  /'
echo "cast hotspots (prod):"
P -c '[^A-Za-z]as [A-Z][A-Za-z]+' | top

echo; echo "## Justification words in comments (prod)"
row "hits" "$(P -c -i '(//|#|\*).*(workaround|hack|for now|temporary|otherwise|todo|fixme)' | sum)"

echo; echo "## History, last $days days"
commits=$(git log --since="$days.days" --oneline | wc -l | tr -d ' ')
reverts=$(git log --since="$days.days" --oneline -i --grep='^revert' | wc -l | tr -d ' ')
fixes=$(git log --since="$days.days" --oneline -i -E --grep='^fix' | wc -l | tr -d ' ')
row "commits" "$commits"
row "reverts" "$reverts"
row "fix commits" "$fixes"
echo "fix churn (files touched by most fix commits):"
git log --since="$days.days" -i -E --grep='^fix' --name-only --format= -- "${paths[@]}" \
  | grep -vE '\.(test|spec|stories)\.|/tests?/|lock|\.md$' | sort | uniq -c | sort -rn | head -8 | sed 's/^/  /'

if [ -n "${CORRECTIONS:-}" ] && [ -f "$CORRECTIONS" ]; then
  echo; echo "## Correction tags"
  awk -F'\t' 'NF>=3 && $2!="" {print $2}' "$CORRECTIONS" | sort | uniq -c | sort -rn | head -10 | sed 's/^/  /'
fi
