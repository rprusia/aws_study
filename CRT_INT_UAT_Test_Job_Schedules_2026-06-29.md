# Copado CRT INT and UAT Test Job Schedules

Pulled from Copado Robotic Testing project `CPQ` on 2026-06-29.

Cron day mapping: `0/7=Sun`, `1=Mon`, `2=Tue`, `3=Wed`, `4=Thu`, `5=Fri`, `6=Sat`.

| Env | Job Name | Job ID | Robot ID | Branch/Tag | Schedule | Timezone | Record | Timeout |
|---|---:|---:|---:|---|---|---|---|---|
| INT | bala_mote_int | 177691 | 11347 | bala_mote | Not scheduled |  |  | 2d |
| INT | ganesh_bommireddy_int | 164954 | 11347 | ganesh_bommireddy | Not scheduled |  |  | 2d |
| UAT | ganesh_bommireddy_uat | 164956 | 11347 | ganesh_bommireddy | Not scheduled |  |  | 2d |
| INT | gupta_anshiki_int | 164955 | 11347 | gupta_anshiki | Not scheduled |  |  | 2d |
| UAT | gupta_anshiki_uat | 164957 | 11347 | gupta_anshiki | Not scheduled |  |  | 2d |
| INT | haramkar_shubham_int | 147368 | 11347 | haramkar_shubham | Not scheduled |  |  | 2d |
| UAT | haramkar_shubham_uat | 147369 | 11347 | haramkar_shubham | Not scheduled |  |  | 2d |
| INT | int_cases | 182968 | 10319 | main | `0 13 * * 0` | Asia/Calcutta | all | 2d |
| INT | int_cl_main_scenarios | 168435 | 10319 | main | `30 0 * * 0,1,2,3,4` | America/New_York | all | 2d |
| INT | int_cl_regression | 172380 | 10319 | main | `15 2 * * 4` | America/New_York | all | 2d |
| INT | int_daily_data | 107741 | 10319 | main | `0 9 * * 0,1,2,3,4,5,6` | America/New_York | all | 2d |
| INT | int_gns_main_scenarios | 96571 | 10319 | main | `10 2 * * 1,2,3,4` | America/New_York | all | 2d |
| INT | int_gns_regression | 93568 | 10319 | main | `0 13 * * 4` | America/New_York | all | 2d |
| INT | int_gov_main_scenarios | 182452 | 10319 | main | `20 4 * * 1,2,3,4` | Etc/UTC | failed | 2d |
| INT | int_igz_main_scenarios | 177381 | 10319 | main | `30 6 * * 1,2,3,4` | Etc/UTC | all | 2d |
| INT | int_igz_regression | 178188 | 10319 | main | `15 2 * * 4` | America/New_York | all | 2d |
| INT | int_juris_main_scenarios | 182454 | 10319 | main | `40 8 * * 1,2,3,4` | Etc/UTC | all | 2d |
| INT | int_ll_main_scenarios | 180499 | 10319 | main | `50 10 * * 1,2,3,4` | Etc/UTC | all | 2d |
| INT | int_ll_regression | 182310 | 10319 | main | `15 2 * * 4` | America/New_York | all | 2d |
| INT | int_pipeline | 35682 | 14095 | main | Not scheduled |  |  | 2d |
| INT | int_regression_cpq | 25953 | 10319 | main | `0 10 * * 4` | America/New_York | all | 2d |
| INT | int_regression_cpq_2 | 65480 | 10319 | main | `0 6 * * 4` | America/Kentucky/Louisville | all | 2d |
| INT | int_rtis_main_scenarios | 112905 | 10319 | main | `0 13 * * 0,1,2,3,4` | America/New_York | all | 2d |
| INT | int_sl_main_scenarios | 25952 | 10319 | main | `10 3 * * 1,2,3,4` | Etc/UTC | all | 2d |
| INT | int_state_net_main_scenarios | 184581 | 10319 | main | `20 17 * * 1,2,3,4` | Etc/UTC | all | 2d |
| INT | int_state_net_regression | 184583 | 10319 | main | `5 2 * * 4` | America/New_York | all | 2d |
| INT | int_uk_main_scenarios | 153796 | 10319 | main | Not scheduled |  |  | 2d |
| INT | int_uk_regression | 152767 | 10319 | main | Not scheduled |  |  | 2d |
| INT | int_usc_main_scenarios | 94549 | 10319 | main | `40 9 * * 2,4` | America/New_York | all | 2d |
| INT | mansi_behl_int | 172036 | 11347 | mansi_behl | Not scheduled |  |  | 2d |
| UAT | mansi_behl_uat | 172632 | 11347 | mansi_behl | Not scheduled |  |  | 2d |
| UAT | mote_bala_uat | 103915 | 11347 | mote_bala | Not scheduled |  |  | 2d |
| INT | parosh_esther_INT | 177573 | 11347 | parosh_esther | Not scheduled |  |  | 2d |
| INT | parosh_esther_int 2 | 171017 | 11347 | parosh_esther | Not scheduled |  |  | 2d |
| UAT | parosh_esther_UAT | 177709 | 11347 | parosh_esther | Not scheduled |  |  | 2d |
| INT | prusia_ray_int | 37812 | 11347 | prusia_ray | Not scheduled |  |  | 2d |
| UAT | prusia_ray_uat | 44861 | 11347 | prusia_ray | Not scheduled |  |  | 2d |
| INT | raja_rajan_int | 188424 | 11347 | raja_rajan | Not scheduled |  |  | 2d |
| UAT | raja_rajan_uat | 179219 | 11347 | raja_rajan | Not scheduled |  |  | 2d |
| INT | ramanan_sreeja_int | 146937 | 11347 | ramanan_sreeja | Not scheduled |  |  | 2d |
| UAT | ramanan_sreeja_uat | 146942 | 11347 | ramanan_sreeja | Not scheduled |  |  | 2d |
| INT | singh_vaibhav_int | 162256 | 11347 | singh_vaibhav | Not scheduled |  |  | 2d |
| UAT | singh_vaibhav_uat | 162257 | 11347 | singh_vaibhav | Not scheduled |  |  | 2d |
| UAT | uat_cases | 182969 | 18471 | main | `0 18 * * 0` | Asia/Calcutta | all | 2d |
| UAT | uat_cl_main_scenarios | 170373 | 18471 | main | `0 1 * * 1,4` | America/New_York | all | 2d |
| UAT | uat_cl_regression | 172381 | 18471 | main | `35 2 * * 4` | America/New_York | all | 2d |
| UAT | uat_daily_data | 71817 | 18471 | main | `0 8 * * 0,1,2,3,4,5,6` | America/New_York | all | 2d |
| UAT | uat_dataLoad_1 | 71069 | 18471 | main | Not scheduled |  |  | 2d |
| UAT | uat_dataLoad_2 | 71777 | 18471 | main | Not scheduled |  |  | 2d |
| UAT | uat_gns_main_scenarios | 98687 | 18471 | main | `10 2 * * 1,4` | America/New_York | all | 2d |
| UAT | uat_gns_regression | 101221 | 18471 | main | `0 1 * * 4` | America/New_York | all | 2d |
| UAT | uat_gov_main_scenarios | 182453 | 18471 | main | `20 4 * * 1,4` | America/New_York | all | 2d |
| UAT | uat_igz_main_scenarios | 178189 | 18471 | main | `0 6 * * 1,4` | America/New_York | all | 2d |
| UAT | uat_igz_regression | 178191 | 18471 | main | `35 2 * * 4` | America/New_York | all | 2d |
| UAT | uat_juris_main_scenarios | 182455 | 18471 | main | `0 2 * * 1,4` | America/New_York | all | 2d |
| UAT | uat_ll_main_scenarios | 181579 | 18471 | main | `30 5 * * 1,4` | America/New_York | all | 2d |
| UAT | uat_ll_regression | 182311 | 18471 | main | `15 2 * * 4` | America/New_York | all | 2d |
| UAT | uat_regression_cpq | 64109 | 18471 | main | `0 11 * * 4` | America/New_York | all | 2d |
| UAT | uat_regression_cpq_2 | 65479 | 18471 | main | `0 14 * * 4` | America/New_York | all | 2d |
| UAT | uat_rtis_main_scenarios | 143980 | 18471 | main | `0 13 * * 1,4` | America/New_York | all | 2d |
| UAT | uat_sl_main_scenarios | 46691 | 18471 | main | `10 3 * * 1,4` | America/New_York | all | 2d |
| UAT | uat_state_net_main_scenarios | 184582 | 18471 | main | `0 1 * * 1,4` | America/New_York | all | 2d |
| UAT | uat_state_net_regression | 184584 | 18471 | main | `0 5 * * 4` | America/New_York | all | 2d |
| UAT | uat_uk_main_scenarios | 162819 | 18471 | main | `30 14 * * 1,4` | America/New_York | all | 2d |
| UAT | uat_uk_regression | 162820 | 18471 | main | `0 0 * * 4` | America/New_York | all | 2d |
| UAT | uat_usc_main_scenario | 186260 | 18471 | main | `0 0 * * 1,4` | America/New_York | all | 2d |

## Counts

- Total INT/UAT jobs: 66
- Scheduled jobs: 40
- Unscheduled jobs: 26
