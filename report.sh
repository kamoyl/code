#!/bin/bash

MAX_PERM_SPACE=$(tail -n1 "${TMP}/${REPORT_FILE3}" | awk -F\~ '{print $4}')
AVG_PERM_SPACE=$(tail -n1 "${TMP}/${REPORT_FILE3}" | awk -F\~ '{print $3}')
SYS_SKEW_FACTOR=$(printf %.2f $(echo "scale=2; 100*(${MAX_PERM_SPACE}-${AVG_PERM_SPACE})/${MAX_PERM_SPACE}" | bc))
echo "~~~~~System skew factor" >> "${TMP}/${REPORT_FILE3}"
echo "~~~~~${SYS_SKEW_FACTOR} %" >> "${TMP}/${REPORT_FILE3}"

echo "" >> "${TMP}/${REPORT_FILE2}"
echo "" >> "${TMP}/${REPORT_FILE2}"
echo "" >> "${TMP}/${REPORT_FILE2}"
echo "" >> "${TMP}/${REPORT_FILE2}"
cat "${TMP}/${REPORT_FILE3}" >> "${TMP}/${REPORT_FILE2}"

inf "Few manipulations for AWT extract data"

#weekly
rm -rf "${TMP}/6_AWT_grid_graph_weekly.out"
for D in {7..1}
do
  DAY=$(date --date="${REPORT_DAY} -${D} day" '+%Y-%m-%d')
  grep -h "^${DAY}" "${TMP}/${REPORT_FILE8}" >> "${TMP}/6_AWT_grid_graph_weekly.out"
done

for DATE in $(awk -F\~ '{print $1}' "${TMP}/6_AWT_grid_graph_weekly.out" | sort -u)
do
  grep -h "^${DATE}" "${TMP}/6_AWT_grid_graph_weekly.out" > "${TMP}/6_AWT_grid_graph_weekly_${DATE}.out"
  cp "${SCRIPTS_HOME}/report_302_transpose.py.bak" "${SCRIPTS_HOME}/report_302_transpose.py"
  sed -i "s/\${DATE}/weekly_${DATE}/g" "${SCRIPTS_HOME}/report_302_transpose.py"
  "${SCRIPTS_HOME}/report_302_transpose.py"
#  sed -i '1d' 6_AWT_grid_graph_transpose_${DATE}.out
  cat "${TMP}/6_AWT_grid_graph_transpose_weekly_${DATE}.out" >> "${TMP}/6_AWT_grid_graph_weekly_result.out"
  echo >> "${TMP}/6_AWT_grid_graph_weekly_result.out"
  echo >> "${TMP}/6_AWT_grid_graph_weekly_result.out"
  rm -rf "${TMP}/6_AWT_grid_graph_weekly_${DATE}.out" "${TMP}/6_AWT_grid_graph_transpose_weekly_${DATE}.out"
done

#monthly
rm -rf "${TMP}/6_AWT_grid_graph_monthly_pivot.out"
"${SCRIPTS_HOME}/report_302_monthly.py"

#daily presentation
for DATE in $(awk -F\~ '{print $1}' "${TMP}/${REPORT_FILE8}" | sort -u)
do
  grep -h "^${DATE}" "${TMP}/${REPORT_FILE8}" > "${TMP}/6_AWT_grid_graph_${DATE}.out"
  cp "${SCRIPTS_HOME}/report_302_transpose.py.bak" "${SCRIPTS_HOME}/report_302_transpose.py"
  sed -i "s/\${DATE}/${DATE}/g" "${SCRIPTS_HOME}/report_302_transpose.py"
  "${SCRIPTS_HOME}/report_302_transpose.py"
#  sed -i '1d' "${TMP}/6_AWT_grid_graph_transpose_${DATE}.out"
  cat "${TMP}/6_AWT_grid_graph_transpose_${DATE}.out" >> "${TMP}/6_AWT_grid_graph_result.out"
  echo >> "${TMP}/6_AWT_grid_graph_result.out"
  echo >> "${TMP}/6_AWT_grid_graph_result.out"
  rm -rf "${TMP}/6_AWT_grid_graph_${DATE}.out" "${TMP}/6_AWT_grid_graph_transpose_${DATE}.out"
done
mv "${TMP}/6_AWT_grid_graph_result.out" "${TMP}/6_AWT_grid_graph_daily.out"
sed -i 's/[[:space:]]*$//g' "${TMP}/6_AWT_grid_graph_daily.out"
mv "${TMP}/6_AWT_grid_graph_monthly_pivot.out" "${TMP}/6_AWT_grid_graph_monthly.out"
mv "${TMP}/6_AWT_grid_graph_weekly_result.out" "${TMP}/6_AWT_grid_graph_weekly.out"

rm -rf "${TMP}/${REPORT_FILE8}"

inf "Extract done"
EMAIL_BODY_LAST=$(echo "")
