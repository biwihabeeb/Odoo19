/** odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart, useRef, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";


const actionRegistry = registry.category("actions");
class InventoryDashboard extends Component {
    setup() {
        super.setup();
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.0/chart.umd.min.js");
            await this._fetchData();

        });
        this.charts = {};
        this.chartRef = useRef("chart_incoming");
        this.chartRefOut = useRef("chart_outgoing");
        this.chartRefInternal = useRef("chart_internal");
        this.chartRefLocation = useRef("chart_location_wise");
        this.chartRefWarehouse = useRef("chart_warehouse");
        this.orm = useService('orm');
        this.actionService = useService('action');
        this.state = useState({
            incoming: false,
            outgoing: false,
            internal: false,
            warehouse: false,
            incomingTotal: 0,
            outgoingTotal: 0,
            internalTotal: 0,
            inventoryValuation: 0,
            period: 0,
            week: 0,
            month: 0,
            year: new Date().getFullYear(),
        });
        onMounted(() => {
            this._renderCharts();
        });
    }
    async _fetchData(){
        const filter = {
            period: this.state.period,
            week: this.state.week,
            month: this.state.month,
            year: this.state.year,
        };
        const incoming = await this.orm.call("stock.move.line","get_incoming_stock",[], {filter});
        const outgoing = await this.orm.call("stock.move.line","get_outgoing_stock",[], {filter});
        const internal = await this.orm.call("stock.move.line","get_internal_transfers",[], {filter});
        const location = await this.orm.call("stock.location","get_stock_location",[], {filter});
        const warehouse = await this.orm.call("stock.warehouse","get_warehouse_locations",[], {filter});
        this.state.incoming = incoming;
        this.state.outgoing = outgoing;
        this.state.internal = internal;
        this.state.location = location;
        this.state.warehouse = warehouse;
        // console.log('compi ',this);

        const moveIds = [];
        const pickingIds = [];
        for(let i = 0; i < this.state.incoming.length; i++){
            moveIds.push(this.state.incoming[i].id);
            // console.log('picking...',this.state.incoming[i].picking_id);
            pickingIds.push(this.state.incoming[i].picking_id[0]);
        }
        this.state.moveIds = moveIds;
        this.state.pickingIds = pickingIds;
        console.log('comp ',this.state.pickingIds);



        var incomingTotal = 0;
        var outgoingTotal = 0;
        var internalTotal = 0;

        for (let i=0; i < incoming.length; i++) {
            incomingTotal += incoming[i].quantity;
        }
        this.state.incomingTotal = incomingTotal;

        for (let i = 0; i < outgoing.length - 2; i++) {
            outgoingTotal += outgoing[i].quantity;
        }
        this.state.outgoingTotal = outgoingTotal;

        for (let i = 0; i < internal.length - 2; i++) {
            internalTotal += internal[i].quantity;
        }
        this.state.internalTotal = internalTotal;
        this._renderCharts();

    }

    viewIncoming() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Incoming Stock Transfers",
            res_model: "stock.move.line",
            domain: [['id','in',this.state.moveIds]],
            views: [[false, 'list'],[false, 'form']]
        })
    }

    viewOutgoing() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Outgoing Stock Transfers",
            res_model: "stock.move.line",
            domain: [['id','in',this.state.outgoing[this.state.outgoing.length-2]]],
            views: [[false, 'list'],[false, 'form']]
        })
    }

    viewInternal(){
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Internal Stock Transfers",
            res_model: "stock.move.line",
            domain: [['id','in',this.state.internal[this.state.internal.length-2]]],
            views: [[false, 'list'],[false, 'form']]
        })
    }

    viewReceipts (){
        // const moveLineIds = this.orm.searchRead('stock.picking',['picking_id'])
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Receipts",
            res_model: "stock.picking",
            domain: [['id','in',this.state.pickingIds]],
            views: [[false, 'list'],[false, 'form']]
        })
    }

    viewDeliveries(){
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Receipts",
            res_model: "stock.picking",
            domain: [['id','in',this.state.outgoing[this.state.outgoing.length-1]]],
            views: [[false, 'list'],[false, 'form']]
        })
    }

    viewInternalTransfer (){
        console.log(this.state.internal[this.state.internal.length-1]);
      this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Receipts",
            res_model: "stock.picking",
            domain: [['id','in',this.state.internal[this.state.internal.length-1]]],
            views: [[false, 'list'],[false, 'form']]
        })
    }

    viewWarehouses(){
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Warehouses",
            res_model: "stock.warehouse",
            views: [[false, 'list'],[false, 'form']]
        })
    }

    viewLocations(){
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Locations",
            res_model: "stock.location",
            views: [[false, 'list'],[false, 'form']]
        })
    }


    async onChangePeriod(){
        await this._fetchData();
        this._renderCharts();
    }
    async onChangeWeek() {
        await this._fetchData();
        this._renderCharts();
    }
    async onChangeMonth(){
        await this._fetchData();
        this._renderCharts();
    }

    _destroyCharts() {

        Object.values(this.charts).forEach((chart) => {
            if (chart) {
                chart.destroy();
            }
        });

        this.charts = {};
    }

    _renderCharts() {

        if (
            !this.chartRef.el ||
            !this.chartRefOut.el ||
            !this.chartRefInternal.el ||
            !this.chartRefLocation.el
        ) {
            return;
        }
        this._destroyCharts();


        this._renderIncomingChart();
        this._renderOutgoingChart();
        this._renderInternalChart();
        this._renderLocationChart();
    }

    _renderIncomingChart(){
        const incomingData = this.state.incoming;
        this.charts.incoming = new Chart(
            this.chartRef.el,
                {
                    type: 'bar',
                    data: {
                        labels: incomingData.map(row => row.product_id[1]),
                        datasets: [
                            {
                                label: 'Incoming Stock',
                                data: incomingData.map(row => row.quantity)
                            }
                        ]
                    }
                });
    }

    _renderOutgoingChart() {
        const outgoingData = this.state.outgoing;
        console.log('OUTGOING::', outgoingData)
        this.charts.outgoing = new Chart(
            this.chartRefOut.el,
                {
                    type: 'bar',
                    data: {
                        labels: outgoingData.map(row => row.product),
                        datasets: [
                            {
                                label: 'Outgoing Stock',
                                data: outgoingData.map(row => row.quantity)
                            }
                        ]
                    }
                }
            );
    }

    _renderInternalChart(){
        const internalData = this.state.internal;
        if(internalData.length != 0 ){
            this.charts.internal = new Chart(
                this.chartRefInternal.el,
                {
                    type: 'bar',
                    data: {
                        labels: internalData.map(row => row.product),
                        datasets: [
                            {
                                label: 'Outgoing Stock',
                                data: internalData.map(row => row.quantity)
                            }
                        ]
                    }
                }
            );
        }

    }

    _renderLocationChart() {
        const locationData = this.state.location;
        this.charts.location = new Chart(
            this.chartRefLocation.el,
                {
                    type: 'line',
                    data: {
                        labels: locationData.map(row => row.location),
                        datasets: [
                            {
                                label: 'Outgoing Stock',
                                data: locationData.map(row => row.quantity)
                            }
                        ]
                    }
                }
            );
    }


}
InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
actionRegistry.add("inventory_dashboard", InventoryDashboard);