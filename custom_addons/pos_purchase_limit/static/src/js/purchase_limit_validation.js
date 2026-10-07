import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { PosStore} from "@point_of_sale/app/services/pos_store";
import { _t } from "@web/core/l10n/translation";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    },
    async validateOrder(isForceValidate){
        const order = this.pos.getOrder();
        const partner = order.partner_id;
        console.log('ORDER: ',order);
        console.log('PARTNER: ',partner.name);
        const capAmount = partner.purchase_limit_amount;
        const orderAmount = order.__lazy_priceExcl;
        console.log('CAP: ',capAmount);
        console.log('ORDERED: ',orderAmount);
        if (!partner){
            this.dialogService.add(AlertDialog, {
                title: _t("No Customer Selected"),
                body: _t("Please select a customer to complete Payment."),
            });
            return;
        }
        if (partner.activate_purchase_limit){
            if (capAmount < orderAmount) {
                this.dialogService.add(AlertDialog, {
                    title: _t("CAP AMOUNT"),
                    body: _t("Customer has exceeded the Purchase Limit Amount.\nCustomer Current Order Amount: %s \nCustomer Purchase Limit Amount: %s",
                         this.env.utils.formatCurrency(orderAmount),
                         this.env.utils.formatCurrency(capAmount)
                    ),
                });
            }
            return;
        }
        console.log('FORCE VALIDATE: ',isForceValidate);
        await super.validateOrder(isForceValidate=true);
    },
});

patch(PosStore.prototype, {
    async pay(){
        console.log('PRODUCT SCREEN');
        const partner = this.__lazy_openOrder.__lazy_partner_id;
        console.log('ORDER PARTNER',partner);
        if (!partner){
            console.log('NO PARTNER');
            this.dialog.add(AlertDialog,{
                title: _t("Customer Not Selected"),
                body: _t("Please Select a Customer to continue"),
            });
            return;
        }

        await super.pay();

    },
});
