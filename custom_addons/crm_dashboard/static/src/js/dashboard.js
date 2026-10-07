/** odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart, useRef, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

const actionRegistry = registry.category("actions");
class CrmDashboard extends Component {
    setup() {
        super.setup();
        onWillStart(async () => {
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.0/chart.umd.min.js")
            await this._fetchData();
        });
        this.charts = {};
        this.chartRefLost = useRef("chart_lost_leads");
        this.chartRefActivities = useRef("chart_activities");
        this.chartRefMedium = useRef("chart_leads_by_medium");
        this.chartRefCampaign = useRef("chart_leads_by_campaign")
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.state = useState({
            leads: 0,
            opportunities: 0,
            revenueExpect: 0,
            revenueEarned: 0,
            winRatio: 0,
            lostLeads: false,
            activities: false,
            leadsMedium: false,
            leadsCampaign: false,
            leadsMonth: false,
            period: 0,
            currency: false
        });
        onMounted(() => {
            this._renderCharts();
        });
    }
    async _fetchData() {
        console.log('FETCHING')
        const val = await this.orm.call("crm.lead","get_dashboard_context",[],{});
        this.state.leads = val.leads_count;
        this.state.opportunities = val.opportunities;
        this.state.revenueExpect = val.expected_revenue;
        this.state.currency = val.currency;
        this.state.revenueEarned =val.earned_revenue;
        this.state.winRatio = val.win_ratio;
        this.state.activities = val.activities;
        this.state.leadsMonth  = val.leads_by_month;
        this.state.leadsMedium = val.leads_by_medium;
        this.state.leadsCampaign = val.leads_by_campaign;
        this.state.lostLeads = val.lost_leads;

        console.log('Val: ',val);
        console.log('State: ',this.state);

    }

    _destroyCharts() {
        Object.values(this.charts).forEach((chart) =>{
            if (chart) {
                chart.destroy();
            }
        });
        this.charts = {};
    }
    _renderActivityChart() {
        const activityData = this.state.activities;
        console.log('RENDER ACTIVITY CHART', activityData);
        this.charts.activities = new Chart(
            this.chartRefActivities.el,
            {
                type: 'doughnut',
                data: {
                    labels: activityData.map(row => row.activity_type.en_US),
                    datasets: [
                        {
                            label: 'Activities',
                            data: activityData.map(row => row.activities)
                        }
                    ]
                }
            }
        )
    }

    _renderMediumLeadsCharts() {
        const leadData = this.state.leadsMedium;
        this.charts.medium = new Chart(
            this.chartRefMedium.el,
            {
                type: 'doughnut',
                data: {
                    labels: leadData.map(row => row.medium),
                    datasets: [
                        {
                            label: 'Leads by Medium',
                            data: leadData.map(row => row.leads)
                        }
                    ]
                }
            }
        )
    }

    _renderCampaignLeadsChart() {
        const leadData = this.state.leadsCampaign;
        console.log('Chart...', leadData)

        this.chartRefCampaign = new Chart(
            this.chartRefCampaign.el,
            {
                type: 'bar',
                data: {
                    labels: leadData.map(row => row.campaign),
                    datasets: [
                        {
                            label: 'Leads by Campaign',
                            data: leadData.map(row => row.leads)
                        }]
                }
            }
        );
    }

    _renderCharts() {
        if (!this.chartRefActivities ||
            !this.chartRefCampaign ||
            !this.chartRefLost ||
            !this.chartRefMedium
        ) {
            return;
        }
        this._destroyCharts();

        this._renderActivityChart();
        this._renderMediumLeadsCharts();
        this._renderCampaignLeadsChart();
    }
}
CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);