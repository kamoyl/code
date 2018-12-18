#!/bin/bash

set -a

RESET=$(tput -T xterm sgr0)

START_BASH_TIME=$(date +%s.%4N)

exec 3>&2 # logging stream (file descriptor 3) defaults to STDERR
verbosity=5 # default to show warnings
silent_lvl=0
crt_lvl=1
err_lvl=2
wrn_lvl=3
inf_lvl=4
dbg_lvl=5

notify() { log ${silent_lvl} "${LIME}NOTE: $1${BLUE}"; } # Always prints
critical() { log ${crt_lvl} "${BRIGHT}${RED}CRITICAL: $1${NORMAL}${BLUE}"; }
error() { log ${err_lvl} "${RED}ERROR: $1${BLUE}"; }
warn() { log ${wrn_lvl} "${WINE}WARNING: $1${BLUE}"; }
inf() { log ${inf_lvl} "${CYAN}INFO: $1${BLUE}"; } # "info" is already a command
debug() { log ${dbg_lvl} "DEBUG: $1"; }
log() {
      if [ ${verbosity} -ge $1 ]
      then
        datestring=$(date +'%H:%M:%S')
        # Expand escaped characters, wrap at 300 chars, indent wrapped lines
        echo -e "${BLUE}${datestring} $(basename $0) [bash_pid: ${$}] ${SHLVL} ${2}${RESET}" | fold -w300 -s | sed '2~1s/^/  /' >&3
      fi
}
export -f inf
export -f debug
export -f warn
export -f critical
export -f notify
export -f error
export -f log
export verbosity

function failed {
  local r=$?
  set +o errtrace
  set +o xtrace
  error "EXIT code: ${YELLOW}${r}${RED} in ${YELLOW}${BASH_SOURCE[1]}${RED} at about ${YELLOW}${BASH_LINENO[0]}${RED}"
}

inf "BASH test, ${BASHPID}"
debug "$0:
SCRIPTS_HOME=${YELLOW}${SCRIPTS_HOME}${BLUE}
TMP=${YELLOW}${TMP}${BLUE}
VAR=${YELLOW}${VAR}${BLUE}
LOG=${YELLOW}${LOG}"

END_BASH_TIME=$(date +%s.%4N)
export BASH_RUNTIME=$(echo "scale=4; x=(${END_BASH_TIME} - ${START_BASH_TIME}); if(x<1) print 0; x" | bc)
inf "BASH script run for: ${BASH_RUNTIME} seconds"
