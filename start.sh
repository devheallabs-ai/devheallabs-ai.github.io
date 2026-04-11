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

case "${1:-}" in
  help|--help|-h)
    banner
    echo -e "${BOLD}Usage:${RESET}"
    echo -e "  ${CYAN}./start.sh${RESET}          Preview website locally on port ${PORT}"
    echo -e "  ${CYAN}./start.sh help${RESET}     Show this help message"
    echo ""
    ;;
  *)
    serve
    ;;
esac
