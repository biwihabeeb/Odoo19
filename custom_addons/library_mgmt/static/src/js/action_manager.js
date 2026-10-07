/** @odoo-module **/
import { registry } from "@web/core/registry";
import { BlockUI } from "@web/core/ui/block_ui";
import { download } from "@web/core/network/download";
// registry.category("ir.actions.report handlers").add("xlsx", async function(acton) {
//     if (action.report_type === 'xlsx'){
//         console.log('in if conditiaon')
//         BlockUI;
//         await download({
//             url: '/xlsx_reports',
//             data: acton.data,
//             complete: () => unblockUI,
//             error: (error) => self.call('crash_manager','rpc_error',error),
//         });
//     }
// });
registry.category("ir.actions.report handlers").add("xlsx", async function (action) {
   if (action.report_type === 'xlsx') {
       BlockUI;
      await download({
              url: '/xlsx_reports',
              data: action.data,
              complete: () => unblockUI,
              error: (error) => self.call('crash_manager', 'rpc_error', error),
              });
   }
});