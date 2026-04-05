#!/usr/bin/env bash
# start.sh — DevHeal Labs website local dev helper
set -euo pipefail

# Colors
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
RESET='\033[0m'

PORT=9000
DIR="$(cd "$(dirname "$0")" && pwd)"

banner() {
  echo ""
  echo -e "${CYAN}${BOLD}  DevHeal Labs AI${RESET}"
  echo -e "${PURPLE}  devheallabs.in${RESET}"
  echo ""
}

serve() {
  banner
  echo -e "${GREEN}Starting local preview server...${RESET}"
  echo ""
  echo -e "  ${BOLD}URL:${RESET}  http://localhost:${PORT}"
  echo -e "  ${BOLD}Dir:${RESET}  ${DIR}"
  echo ""
  echo -e "${YELLOW}Press Ctrl+C to stop.${RESET}"
  echo ""
  cd "$DIR"
  python3 -m http.server "$PORT"
}

deploy_instructions() {
  banner
  echo -e "${BOLD}Deploy to GitHub Pages${RESET}"
  echo ""
  echo -e "  ${CYAN}1.${RESET} Clone the deployment repo (if not already):"
  echo -e "     ${PURPLE}git clone git@github.com:DevHealLabs/devheallabs.github.io.git${RESET}"
  echo ""
  echo -e "  ${CYAN}2.${RESET} Copy files to the deployment repo:"
  echo -e "     ${PURPLE}cp ${DIR}/index.html ${DIR}/404.html ${DIR}/CNAME <deploy-repo>/${RESET}"
  echo ""
  echo -e "  ${CYAN}3.${RESET} Commit and push:"
  echo -e "     ${PURPLE}cd <deploy-repo>${RESET}"
  echo -e "     ${PURPLE}git add -A${RESET}"
  echo -e "     ${PURPLE}git commit -m \"Update website\"${RESET}"
  echo -e "     ${PURPLE}git push origin main${RESET}"
  echo ""
  echo -e "${GREEN}GitHub Pages will deploy automatically within a few minutes.${RESET}"
  echo ""
}

case "${1:-}" in
  deploy)
    deploy_instructions
    ;;
  help|--help|-h)
    banner
    echo -e "${BOLD}Usage:${RESET}"
    echo -e "  ${CYAN}./start.sh${RESET}          Preview website locally on port ${PORT}"
    echo -e "  ${CYAN}./start.sh deploy${RESET}   Show deployment instructions"
    echo -e "  ${CYAN}./start.sh help${RESET}     Show this help message"
    echo ""
    ;;
  *)
    serve
    ;;
esac
