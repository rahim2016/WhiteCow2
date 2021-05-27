const MonthlyDealNuber = document.querySelector('#monthy_number');
const DailyDealNuber = document.querySelector('#daily_number');
const AnnualDealNuber = document.querySelector('#annual_number');
const annual_deal_chart = document.querySelector('#annual_deal_chart');
const monthly_deal_chart = document.querySelector('#monthly_deal_chart');
const daily_deal_chart = document.querySelector('#daily_deal_chart');

var land ;
var multi_family ;
var single_family;
var mobile ;
var farm ;
var num ;
var re = [];

const getChartData = () => {
   fetch("/deal_stats").then((res)=> res.json()).then((results)=>{

        console.log("loading", results.deal_category_data.month)
        MonthlyDealNuber.innerHTML = results.deal_category_data.month;
        DailyDealNuber.innerHTML = results.deal_category_data.day;
        AnnualDealNuber.innerHTML = results.deal_category_data.year;
        annual_deal_chart.value = results.deal_category_data.year;
        monthly_deal_chart.value = results.deal_category_data.month;
        daily_deal_chart.value = results.deal_category_data.day;

        land = results.deal_category_data.land;
        multi_family = results.deal_category_data.multi_family;
        single_family = results.deal_category_data.single_family;
        mobile = results.deal_category_data.mobile;
        farm = results.deal_category_data.farm;
        year_2021 = results.deal_category_data.year_2021;
        re.push(land);
        re.push(mobile);
        re.push(single_family);

        console.log("land", land);
        console.log("single_family", single_family);

        
        
    




        !function(e) {


            "use strict";
            var a = function() { this.$realData = [] };
            a.prototype.createBarChart = function(e, a, r, t, o, i) { 
            Morris.Bar({ 
                element: e, data: a, xkey: r, ykeys: t, labels: o, hideHover: "auto", resize: !0, gridLineColor: "rgba(173, 181, 189, 0.1)", barSizeRatio: .2, dataLabels: !1, barColors: i }) }, 
                a.prototype.createLineChart = function(e, a, r, t, o, i, n, l, s) { 
                    Morris.Line({ element: e, data: a, xkey: r, ykeys: t, labels: o, fillOpacity: i, pointFillColors: n, pointStrokeColors: l, behaveLikeLine: !0, gridLineColor: "rgba(173, 181, 189, 0.1)", hideHover: "auto", resize: !0, pointSize: 0, dataLabels: !1, lineColors: s }) }, a.prototype.createDonutChart = function(e, a, r) { 
                        
                    Morris.Donut({ element: e, data: a, resize: !0, colors: r, backgroundColor: "transparent" }) }, a.prototype.init = function() {
            this.createBarChart("morris-bar-example", [{ y: "2019", a: 0 }, { y: "2020", a: 0}, { y: "2021", a: year_2021}, { y: "2022", a: 0 }], "y", ["a"], ["Statistics"], ["#188ae2"]);
           
            this.createDonutChart("morris-donut-example", [{ label: "Single Family", value: single_family}, { label: "Land", value: land }, { label: "Multi Family", value: multi_family }, { label: "Mobile", value: mobile }, { label: "Farm", value: farm }], ["#5b69bc", "#ff8acc","#b5bc5b", "#060627", "#dda53c"])
            }, e.Dashboard1 = new a, e.Dashboard1.Constructor = a
            }(window.jQuery),
            function(e) {
            "use strict";
            window.jQuery.Dashboard1.init()
            }();
        
    });
    

     
};







document.onload = getChartData();





