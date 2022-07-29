odoo.define('mate_elearning.OMDashboard', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var web_client = require('web.web_client');
    var session = require('web.session');
    var _t = core._t;
    var QWeb = core.qweb;
    var self = this;
    var currency;
    var DashBoard = AbstractAction.extend({
        contentTemplate: 'OMDashboard',
        events: {
            'change #income_expense_values': function (e) {
                e.stopPropagation();
                var $target = $(e.target);
                var value = $target.val();
                this.cardDashboardData(value);
                // else if (value == "this_quarter") {
                //     this.onclick_this_quarter($target.val());
                // } else if (value == "this_month") {
                //     this.onclick_this_month($target.val());
                // } else if (value == "this_week") {
                //     this.onclick_this_week($target.val());
                // }
            },
//            'change #total_loosed_crm_sub': function(e) {
//                e.stopPropagation();
//                var $target = $(e.target);
//                var value = $target.val();
//                if (value=="sub_lost_last_12months"){
//                    this.onclick_sub_lost_last_12months($target.val());
//                }else if (value=="sub_lost_last_6months"){
//                    this.onclick_sub_lost_last_6months($target.val());
//                }else if (value=="sub_lost_last_month"){
//                    this.onclick_sub_lost_last_month($target.val());
//                }
//            },
        },

        init: function (parent, context) {
            this._super(parent, context);
            this.upcoming_events = [];
//            this.dashboards_templates = ['LoginUser','Managercrm','Admincrm', 'SubDashboard'];
            this.dashboards_templates = ['dashboard'];
            this.login_employee = [];
        },


        start: function () {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function () {
                self.update_cp();
                self.render_dashboards();
                self.funnel_chart();
                self.$el.parent().addClass('oe_background_grey');
                self.cardDashboardData('this_week');
                self.topRankExam();
                self.topCourse();
                self.topSurveyExam();
                self.topSurveyUser();
                self.toCalendar();
            });
        },

        toCalendar: function () {
            $(document).ready(function () {
                $('.input-daterange').datepicker({
                    format: 'dd/mm',
                    autoclose: true
                });
            });
        },

        topRankExam: function () {
            var self = this;
            rpc.query({
                model: 'mate_elearning.dashboard',
                method: 'get_top_survey_exam_department',
                args: [],
            })
                .then(function (result) {
                    $('.top5_train h6').text(result.top_survey_exam_name);
                    $('.top5_train p').text(result.top_survey_exam_job);
                    $('.top5_train .content_percent').text(result.top_survey_exam_percent + '%');
                })
        },

        topCourse: function () {
            var self = this;
            rpc.query({
                model: 'mate_elearning.dashboard',
                method: 'get_top_course',
                args: [],
            })
                .then(function (result) {
                    $('.get_top_course_top1_class h6').text(result.get_top_course_name_top1);
                    $('.get_top_course_top2_class h6').text(result.get_top_course_name_top2);
                    $('.get_top_course_top3_class h6').text(result.get_top_course_name_top3);
                    $('.get_top_course_top4_class h6').text(result.get_top_course_name_top4);
                    $('.get_top_course_top5_class h6').text(result.get_top_course_name_top5);

                    $('.get_top_course_top1_class p').text(result.get_top_course_top1_channel_type);
                    $('.get_top_course_top2_class p').text(result.get_top_course_top2_channel_type);
                    $('.get_top_course_top3_class p').text(result.get_top_course_top3_channel_type);
                    $('.get_top_course_top4_class p').text(result.get_top_course_top4_channel_type);
                    $('.get_top_course_top5_class p').text(result.get_top_course_top5_channel_type);

                    $('.get_top_course_top1_class .content_percent').text(result.course_percentage_top1 + '%');
                    $('.get_top_course_top2_class .content_percent').text(result.course_percentage_top2 + '%');
                    $('.get_top_course_top3_class .content_percent').text(result.course_percentage_top3 + '%');
                    $('.get_top_course_top4_class .content_percent').text(result.course_percentage_top4 + '%');
                    $('.get_top_course_top5_class .content_percent').text(result.course_percentage_top5 + '%');
                })
        },

        topSurveyExam: function () {
            var self = this;
            rpc.query({
                model: 'mate_elearning.dashboard',
                method: 'get_top_survey_exam',
                args: [],
            })
                .then(function (result) {
                    $('.get_top_survey_exam_top1_class h6').text(result.get_top_survey_exam_name_top1);
                    $('.get_top_survey_exam_top2_class h6').text(result.get_top_survey_exam_name_top2);
                    $('.get_top_survey_exam_top3_class h6').text(result.get_top_survey_exam_name_top3);
                    $('.get_top_survey_exam_top4_class h6').text(result.get_top_survey_exam_name_top4);
                    $('.get_top_survey_exam_top5_class h6').text(result.get_top_survey_exam_name_top5);

                    $('.get_top_survey_exam_top1_class p').text(result.get_top_survey_exam_top1_channel_type);
                    $('.get_top_survey_exam_top2_class p').text(result.get_top_survey_exam_top2_channel_type);
                    $('.get_top_survey_exam_top3_class p').text(result.get_top_survey_exam_top3_channel_type);
                    $('.get_top_survey_exam_top4_class p').text(result.get_top_survey_exam_top4_channel_type);
                    $('.get_top_survey_exam_top5_class p').text(result.get_top_survey_exam_top5_channel_type);

                    $('.get_top_survey_exam_top1_class .content_percent').text(result.survey_exam_percentage_top1 + '%');
                    $('.get_top_survey_exam_top2_class .content_percent').text(result.survey_exam_percentage_top2 + '%');
                    $('.get_top_survey_exam_top3_class .content_percent').text(result.survey_exam_percentage_top3 + '%');
                    $('.get_top_survey_exam_top4_class .content_percent').text(result.survey_exam_percentage_top4 + '%');
                    $('.get_top_survey_exam_top5_class .content_percent').text(result.survey_exam_percentage_top5 + '%');
                })
        },

        topSurveyUser: function () {
            var self = this;
            rpc.query({
                model: 'mate_elearning.dashboard',
                method: 'get_top_survey_user',
                args: [],
            })
                .then(function (result) {
                    $('.get_top_survey_user_input_top1_class h6').text(result.get_top_survey_user_input_name_top1);
                    $('.get_top_survey_user_input_top2_class h6').text(result.get_top_survey_user_input_name_top2);
                    $('.get_top_survey_user_input_top3_class h6').text(result.get_top_survey_user_input_name_top3);
                    // $('.get_top_survey_user_input_top4_class h6').text(result.get_top_survey_user_input_name_top4);
                    // $('.get_top_survey_user_input_top5_class h6').text(result.get_top_survey_user_input_name_top5);
                    //
                    $('.get_top_survey_user_input_top1_class p').text(result.get_top_survey_user_input_top1_channel_type);
                    $('.get_top_survey_user_input_top2_class p').text(result.get_top_survey_user_input_top2_channel_type);
                    $('.get_top_survey_user_input_top3_class p').text(result.get_top_survey_user_input_top3_channel_type);
                    // $('.get_top_survey_user_input_top4_class p').text(result.get_top_survey_user_input_top4_channel_type);
                    // $('.get_top_survey_user_input_top5_class p').text(result.get_top_survey_user_input_top5_channel_type);
                    //
                    $('.get_top_survey_user_input_top1_class .content_percent').text(result.survey_user_input_percentage_top1 + '%');
                    $('.get_top_survey_user_input_top2_class .content_percent').text(result.survey_user_input_percentage_top2 + '%');
                    $('.get_top_survey_user_input_top3_class .content_percent').text(result.survey_user_input_percentage_top3 + '%');
                    // $('.get_top_survey_user_input_top4_class .content_percent').text(result.survey_user_input_percentage_top4 + '%');
                    // $('.get_top_survey_user_input_top5_class .content_percent').text(result.survey_user_input_percentage_top5 + '%');
                })
        },


        cardDashboardData: function (value) {
            var self = this;
            rpc.query({
                model: 'mate_elearning.dashboard',
                method: 'mate_elearning_' + value,
                args: [],
            })
                .then(function (result) {
                    // Tổng người dùng
                    $('#total_user h3').text(result.record_total_user_moment);
                    $('#total_user .total_user_growth').text(result.record_total_user_growth + '%');
                    $('.total_user_growth').attr('class', result.record_total_user_growth >= 0 ? 'total_user_growth growth_max' : 'total_user_growth growth_min')
                    $('#total_user .icon_number .green').attr('class', result.record_total_user_growth >= 0 ? 'total_user icon_number green growth_max_img_green' : 'total_user icon_number green growth_min_img_green')
                    $('#total_user .icon_number .red').attr('class', result.record_total_user_growth >= 0 ? 'total_user icon_number red growth_max_img_red' : 'total_user icon_number red growth_min_img_red')
                    // Khóa học
                    $('#course h3').text(result.record_course_moment);
                    $('#course .course_growth').text(result.record_course_growth + '%');
                    $('.course_growth').attr('class', result.record_course_growth >= 0 ? 'course_growth growth_max' : 'course_growth growth_min')
                    $('#course .icon_number .green').attr('class', result.record_course_growth >= 0 ? 'course icon_number green growth_max_img_green' : 'course icon_number green growth_min_img_green')
                    $('#course .icon_number .red').attr('class', result.record_course_growth >= 0 ? 'course icon_number red growth_max_img_red' : 'course icon_number red growth_min_img_red')
                    // Kỳ thi
                    $('#survey_exam h3').text(result.record_survey_exam_moment);
                    $('#survey_exam .survey_exam_growth').text(result.record_survey_exam_growth + '%');
                    $('.survey_exam_growth').attr('class', result.record_survey_exam_growth >= 0 ? 'survey_exam_growth growth_max' : 'survey_exam_growth growth_min')
                    $('#survey_exam .icon_number .green').attr('class', result.record_survey_exam_growth >= 0 ? 'survey_exam icon_number green growth_max_img_green' : 'survey_exam icon_number green growth_min_img_green')
                    $('#survey_exam .icon_number .red').attr('class', result.record_survey_exam_growth >= 0 ? 'survey_exam icon_number red growth_max_img_red' : 'survey_exam icon_number red growth_min_img_red')
                    // Bài khảo sát
                    $('#survey_survey h3').text(result.record_survey_survey_moment);
                    $('#survey_survey .survey_survey_growth').text(result.record_survey_survey_growth + '%');
                    $('.survey_survey_growth').attr('class', result.record_survey_survey_growth >= 0 ? 'survey_survey_growth growth_max' : 'survey_survey_growth growth_min')
                    $('#survey_survey .icon_number .green').attr('class', result.record_survey_survey_growth >= 0 ? 'survey_survey icon_number green growth_max_img_green' : 'survey_survey icon_number green growth_min_img_green')
                    $('#survey_survey .icon_number .red').attr('class', result.record_survey_survey_growth >= 0 ? 'survey_survey icon_number red growth_max_img_red' : 'survey_survey icon_number red growth_min_img_red')
                    // Câu hỏi
                    $('#total_question h3').text(result.record_total_question_moment);
                    $('#total_question .total_question_growth').text(result.record_total_question_growth + '%');
                    $('.total_question_growth').attr('class', result.record_total_question_growth >= 0 ? 'total_question_growth growth_max' : 'total_question_growth growth_min')
                    $('#total_question .icon_number .green').attr('class', result.record_total_question_growth >= 0 ? 'total_question icon_number green growth_max_img_green' : 'total_question icon_number green growth_min_img_green')
                    $('#total_question .icon_number .red').attr('class', result.record_total_question_growth >= 0 ? 'total_question icon_number red growth_max_img_red' : 'total_question icon_number red growth_min_img_red')
                })
        },

        funnel_chart: function () {
            var seriesTitle = [["20/6"], ["21/6"], ["22/6"], ["23/6"], ["24/6"], ["25/6"], ["26/6"]];
            var seriesDataLogIn = [[47], [87], [49], [50], [40], [52], [68]];
            var seriesDataRegister = [[37], [76], [39], [60], [30], [62], [48]];
            var seriesDataCompletedTheCourse = [[57], [97], [39], [20], [50], [72], [38]];

            setTimeout(function () {
                    Highcharts.chart('container', {
                        chart: {
                            type: 'areaspline',
                        },
                        title: {
                            text: ''
                        },
                        legend: {
                            margin: 30
                        },
                        xAxis: {
                            tickLength: 0,
                            minPadding: 0,
                            maxPadding: 0,
                            tickInterval: 1,
                            labels: {
                                enabled: true,
                                formatter: function () {
                                    return seriesTitle[this.value][0];
                                },
                                useHTML: true,
                                style: {
                                    paddingTop: '15px',
                                    fontFamily: 'Inter,sans-serif',
                                    fontStyle: 'normal',
                                    fontWeight: '600',
                                    fontSize: '16px',
                                    color: '#3F4346',
                                }
                            },
                        },
                        plotOptions: {
                            series: {},
                        },

                        yAxis: {
                            labels: {
                                useHTML: true,
                                style: {
                                    fontFamily: 'Inter,sans-serif',
                                    fontStyle: 'normal',
                                    fontWeight: '600',
                                    fontSize: '16px',
                                    color: '#3F4346',
                                }
                            },
                            title: {
                                text: ''
                            },
                        },

                        tooltip: {
                            backgroundColor: '#F4F4F4',
                            borderWidth: '1',
                            borderColor: '#DBDBDB',
                            borderRadius: '12',
                            padding: 16,
                            shadow: '4px 8px 24px rgba(23, 22, 22, 0.08)',
                            shared: true,
                            useHTML: true,
                            headerFormat: '<div style="display: none"></div>',
                            pointFormat: '<div class="tooltip_custom" style="display: flex;align-items: center;padding-bottom: 12px">' +
                                '<div class="box_tooltip" style="width: 16px;height: 16px;border-radius: 4px;border: 1px solid {point.color}; background-color: {point.color}"></div>' +
                                '<div class="text_tooltip" style="font-family: \'Inter\', sans-serif;font-style: normal;line-height: 24px;height: 24px;font-weight: 600;font-size: 14px; #3F4346;padding-left: 8px">{series.name}: {point.y}</div>' +
                                '</div>',
                            valueSuffix: 'ng',

                        },

                        colors: ['#1D93CD', '#E16565', '#11A829'],

                        credits: {
                            enabled: false
                        },

                        series: [{
                            name: "Đăng nhập",
                            data: seriesDataCompletedTheCourse,
                            lineWidth: 4,
                            lineColor: '#1D93CD',
                            fillColor: 'none',
                            marker: {
                                fillColor: '#F4F4F4',
                                lineWidth: 3,
                                lineColor: '#1D93CD',
                                enabled: false,
                                symbol: 'circle'
                            }
                        }, {
                            name: "Đăng ký",
                            data: seriesDataRegister,
                            lineWidth: 4,
                            lineColor: '#E16565',
                            fillColor: 'none',
                            marker: {
                                fillColor: '#F4F4F4',
                                lineWidth: 3,
                                lineColor: '#E16565',
                                enabled: false,
                                symbol: 'circle'
                            }
                        }, {
                            name: "Hoàn thành khóa học",
                            data: seriesDataLogIn,
                            lineWidth: 4,
                            lineColor: '#11A829',
                            fillColor: 'none',
                            marker: {
                                fillColor: '#F4F4F4',
                                lineWidth: 3,
                                lineColor: '#11A829',
                                enabled: false,
                                symbol: 'circle'
                            }
                        }],
                    });
                    // start
                    var chart = $('#container').highcharts();

                    $('.checkbox').on('change', function () {
                        for (var i = 0; i < $('input[type=checkbox]').length; i++) {
                            var series = chart.series[i];

                            if ($('#check' + i).is(':checked')) {
                                series.show();
                            } else {
                                series.hide();
                            }
                        }
                    });
                    // end
                }
                ,
                1000
            )
        }
        ,

        render_dashboards: function () {
            var self = this;
            if (this.login_employee) {
                var templates = []
                if (self.is_manager === true) {
//                    templates = ['LoginUser', 'Managercrm', 'Admincrm', 'SubDashboard'];
                    templates = ['dashboard'];
                } else {
                    templates = ['dashboard'];
                }
                _.each(templates, function (template) {
                    self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}));
                });
            } else {
                self.$('.o_hr_dashboard').append(QWeb.render('EmployeeWarning', {widget: self}));
            }
        }
        ,

        update_cp: function () {
            var self = this;
        }
        ,
    });

    core.action_registry.add('mate_elearning', DashBoard);
    return DashBoard;
})
;