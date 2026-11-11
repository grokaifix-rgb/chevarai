#!/bin/bash
# Chevar AI — botni yangi Railway hisobiga ko'chirish.
# Oldin: 1) eski botdan /zaxira olingan  2) `railway login` bilan YANGI hisobga kirilgan.
set -e
cd "$(dirname "$0")"
[ -f .env.railway ] || { echo ".env.railway topilmadi"; exit 1; }
echo "Hisob: $(railway whoami 2>&1 | head -1)"
rm -rf .railway
railway init --name chevar-ai --json
railway add --service chevar-ai
railway service chevar-ai
ARGS=()
while IFS= read -r q; do [ -n "$q" ] && ARGS+=(--set "$q"); done < .env.railway
railway variables --skip-deploys "${ARGS[@]}" >/dev/null
railway volume add -m /data
railway up --ci --service chevar-ai
railway service source connect --repo grokaifix-rgb/chevarai --branch main --service chevar-ai || \
  echo "GitHub ulanmadi — keyin Railway sahifasida ulang"
railway logs --service chevar-ai | tail -5
echo "Tayyor. Endi botga /tiklash yozib, zaxira faylini yuboring."
