# from odoo import api, fields, models
#
import datetime
import calendar

from odoo import models, fields, api
from odoo.tools import date_utils
from odoo.http import request

from dateutil.relativedelta import relativedelta
from datetime import datetime


class MateElearningDashboard(models.Model):
    _name = 'mate_elearning.dashboard'

    @api.model
    def mate_elearning_this_year(self):

        # Tổng người dùng

        self._cr.execute('''select COUNT(id) from slide_channel_partner  WHERE Extract(Year FROM slide_channel_partner.create_date)
         = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_channel_partner_value_moment = rec_ids_moment[0]

        self._cr.execute('''select COUNT(id) from slide_channel_partner
                                WHERE date_trunc('year', DATE(slide_channel_partner.create_date)) = date_trunc('year', DATE(NOW()) - interval '1 year')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_channel_partner_value_ago = rec_ids_ago[0]

        if slide_channel_partner_value_ago == 0:
            slide_channel_partner_value_growth = slide_channel_partner_value_moment * 100
        else:
            slide_channel_partner_value_growth = (((
            slide_channel_partner_value_moment - slide_channel_partner_value_ago) / abs(
            slide_channel_partner_value_ago)) * 100)

        # Khóa học

        self._cr.execute('''select COUNT(id) from slide_slide WHERE Extract(Year FROM slide_slide.create_date)
                 = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_slide_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from slide_slide 
            WHERE date_trunc('year', DATE(slide_slide.create_date)) = date_trunc('year', DATE(NOW()) - interval '1 year')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_slide_value_ago = rec_ids_ago[0]

        if slide_slide_value_ago == 0:
            slide_slide_value_growth = slide_slide_value_moment * 100
        else:
            slide_slide_value_growth = (
                    ((slide_slide_value_moment - slide_slide_value_ago) / abs(slide_slide_value_ago)) * 100)

        # Kỳ thi

        self._cr.execute('''select COUNT(id) from survey_survey 
        WHERE certification = true AND Extract(Year FROM survey_survey.create_date)
                         = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_exam_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_survey 
            WHERE certification = true AND date_trunc('year', DATE(survey_survey.create_date)) = date_trunc('year', DATE(NOW()) - interval '1 year')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_exam_value_ago = rec_ids_ago[0]

        if survey_exam_value_ago == 0:
            survey_exam_value_growth = survey_exam_value_moment * 100
        else:
            survey_exam_value_growth = (
                    ((survey_exam_value_moment - survey_exam_value_ago) / abs(survey_exam_value_ago)) * 100)

        # Bài khảo sát

        self._cr.execute('''select COUNT(id) from survey_survey 
        WHERE certification = false AND Extract(Year FROM survey_survey.create_date)
                                 = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_survey_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_survey 
            WHERE certification = false AND date_trunc('year', DATE(survey_survey.create_date)) = date_trunc('year', DATE(NOW()) - interval '1 year')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_survey_value_ago = rec_ids_ago[0]

        if survey_survey_value_ago == 0:
            survey_survey_value_growth = survey_survey_value_moment * 100
        else:
            survey_survey_value_growth = (
                    ((survey_survey_value_moment - survey_survey_value_ago) / abs(survey_survey_value_ago)) * 100)

        # Câu hỏi

        self._cr.execute('''select COUNT(id) from survey_question 
        WHERE Extract(Year FROM survey_question.create_date)
                                         = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_question_value_moment = rec_ids_moment[0]

        self._cr.execute('''select COUNT(id) from slide_question 
        WHERE Extract(Year FROM slide_question.create_date)
                                                 = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_question_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_question 
            WHERE date_trunc('year', DATE(survey_question.create_date)) = date_trunc('year', DATE(NOW()) - interval '1 year')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_question_value_ago = rec_ids_ago[0]

        self._cr.execute(
            '''select COUNT(id) from slide_question 
            WHERE date_trunc('year', DATE(slide_question.create_date)) = date_trunc('year', DATE(NOW()) - interval '1 year')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_question_value_ago = rec_ids_ago[0]

        total_question_moment = survey_question_value_moment + slide_question_value_moment

        total_question_ago = survey_question_value_ago + slide_question_value_ago

        if total_question_ago == 0:
            total_question_growth = total_question_moment * 100
        else:
            total_question_growth = (
                    ((total_question_moment - total_question_ago) / abs(total_question_ago)) * 100)

        data_year = {
            # Tổng người dùng
            'record_total_user_moment': slide_channel_partner_value_moment,
            'record_total_user_ago': slide_channel_partner_value_ago,
            'record_total_user_growth': round(slide_channel_partner_value_growth, 2),
            # Khóa học
            'record_course_moment': slide_slide_value_moment,
            'record_course_ago': slide_slide_value_ago,
            'record_course_growth': round(slide_slide_value_growth, 2),
            # Kỳ thi
            'record_survey_exam_moment': survey_exam_value_moment,
            'record_survey_exam_ago': survey_exam_value_ago,
            'record_survey_exam_growth': round(survey_exam_value_growth, 2),
            # Bài khảo sát
            'record_survey_survey_moment': survey_survey_value_moment,
            'record_survey_survey_ago': survey_survey_value_ago,
            'record_survey_survey_growth': round(survey_survey_value_growth, 2),
            # Câu hỏi
            'record_total_question_moment': total_question_moment,
            'record_total_question_ago': total_question_ago,
            'record_total_question_growth': round(total_question_growth, 2),

        }
        return data_year

    @api.model
    def mate_elearning_this_quarter(self):

        # Tổng người dùng

        self._cr.execute('''select COUNT(id) from slide_channel_partner WHERE Extract(QUARTER FROM slide_channel_partner.create_date) = Extract(QUARTER FROM DATE(NOW()))
        AND Extract(Year FROM slide_channel_partner.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_channel_partner_value_moment = rec_ids_moment[0]

        self._cr.execute('''select COUNT(id) from slide_channel_partner
                        WHERE date_trunc('quarter', DATE(slide_channel_partner.create_date)) = date_trunc('quarter', DATE(NOW()) - interval '3 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_channel_partner_value_ago = rec_ids_ago[0]

        if slide_channel_partner_value_ago == 0:
            slide_channel_partner_value_growth = slide_channel_partner_value_moment * 100
        else:
            slide_channel_partner_value_growth = (((
                                                           slide_channel_partner_value_moment - slide_channel_partner_value_ago) / abs(
                slide_channel_partner_value_ago)) * 100)

        # Khóa học

        self._cr.execute('''select COUNT(id) from slide_slide WHERE Extract(QUARTER FROM slide_slide.create_date) = Extract(QUARTER FROM DATE(NOW()))
                AND Extract(Year FROM slide_slide.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_slide_value_moment = rec_ids_moment[0]

        self._cr.execute('''select COUNT(id) from slide_slide
                                WHERE date_trunc('quarter', DATE(slide_slide.create_date)) = date_trunc('quarter', DATE(NOW()) - interval '3 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_slide_value_ago = rec_ids_ago[0]

        if slide_slide_value_ago == 0:
            slide_slide_value_growth = slide_slide_value_moment * 100
        else:
            slide_slide_value_growth = (
                    ((slide_slide_value_moment - slide_slide_value_ago) / abs(slide_slide_value_ago)) * 100)

        # Kỳ thi

        self._cr.execute('''select COUNT(id) from survey_survey WHERE certification = true AND Extract(QUARTER FROM survey_survey.create_date) = Extract(QUARTER FROM DATE(NOW()))
            AND Extract(Year FROM survey_survey.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_exam_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_survey
                            WHERE certification = true AND date_trunc('quarter', DATE(survey_survey.create_date)) = date_trunc('quarter', DATE(NOW()) - interval '3 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_exam_value_ago = rec_ids_ago[0]

        if survey_exam_value_ago == 0:
            survey_exam_value_growth = survey_exam_value_moment * 100
        else:
            survey_exam_value_growth = (
                    ((survey_exam_value_moment - survey_exam_value_ago) / abs(survey_exam_value_ago)) * 100)

        # Bài khảo sát

        self._cr.execute(
            '''select COUNT(id) from survey_survey WHERE certification = false AND Extract(QUARTER FROM survey_survey.create_date) = Extract(QUARTER FROM DATE(NOW())) AND Extract(Year FROM survey_survey.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_survey_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_survey WHERE certification = false AND date_trunc('quarter', DATE(survey_survey.create_date)) = date_trunc('quarter', DATE(NOW()) - interval '3 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_survey_value_ago = rec_ids_ago[0]

        if survey_survey_value_ago == 0:
            survey_survey_value_growth = survey_survey_value_moment * 100
        else:
            survey_survey_value_growth = (
                    ((survey_survey_value_moment - survey_survey_value_ago) / abs(survey_survey_value_ago)) * 100)

        # Câu hỏi

        self._cr.execute(
            '''select COUNT(id) from slide_question WHERE Extract(QUARTER FROM slide_question.create_date) = Extract(QUARTER FROM DATE(NOW())) AND Extract(Year FROM slide_question.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_question_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_question WHERE Extract(QUARTER FROM survey_question.create_date) = Extract(QUARTER FROM DATE(NOW())) AND Extract(Year FROM survey_question.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_question_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from slide_question WHERE date_trunc('quarter', DATE(slide_question.create_date)) = date_trunc('quarter', DATE(NOW()) - interval '3 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_question_value_ago = rec_ids_ago[0]

        self._cr.execute(
            '''select COUNT(id) from survey_question WHERE date_trunc('quarter', DATE(survey_question.create_date)) = date_trunc('quarter', DATE(NOW()) - interval '3 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_question_value_ago = rec_ids_ago[0]

        total_question_moment = survey_question_value_moment + slide_question_value_moment

        total_question_ago = survey_question_value_ago + slide_question_value_ago

        if total_question_ago == 0:
            total_question_growth = total_question_moment * 100
        else:
            total_question_growth = (
                    ((total_question_moment - total_question_ago) / abs(total_question_ago)) * 100)

        data_quarter = {
            # Tổng người dùng
            'record_total_user_moment': slide_channel_partner_value_moment,
            'record_total_user_ago': slide_channel_partner_value_ago,
            'record_total_user_growth': round(slide_channel_partner_value_growth, 2),
            # Khóa học
            'record_course_moment': slide_slide_value_moment,
            'record_course_ago': slide_slide_value_ago,
            'record_course_growth': round(slide_slide_value_growth, 2),
            # Kỳ thi
            'record_survey_exam_moment': survey_exam_value_moment,
            'record_survey_exam_ago': survey_exam_value_ago,
            'record_survey_exam_growth': round(survey_exam_value_growth, 2),
            # Bài khảo sát
            'record_survey_survey_moment': survey_survey_value_moment,
            'record_survey_survey_ago': survey_survey_value_ago,
            'record_survey_survey_growth': round(survey_survey_value_growth, 2),
            # Câu hỏi
            'record_total_question_moment': total_question_moment,
            'record_total_question_ago': total_question_ago,
            'record_total_question_growth': round(total_question_growth, 2),
        }
        return data_quarter

    @api.model
    def mate_elearning_this_month(self):

        # Tổng người dùng

        self._cr.execute('''select COUNT(id) from slide_channel_partner WHERE Extract(MONTH FROM slide_channel_partner.create_date) = Extract(MONTH FROM DATE(NOW()))
        AND Extract(Year FROM slide_channel_partner.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_channel_partner_value_moment = rec_ids_moment[0]

        self._cr.execute('''select COUNT(id) from slide_channel_partner
                WHERE date_trunc('month', DATE(slide_channel_partner.create_date)) = date_trunc('month', DATE(NOW()) - interval '1 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_channel_partner_value_ago = rec_ids_ago[0]

        if slide_channel_partner_value_ago == 0:
            slide_channel_partner_value_growth = slide_channel_partner_value_moment * 100
        else:
            slide_channel_partner_value_growth = (((
                                                           slide_channel_partner_value_moment - slide_channel_partner_value_ago) / abs(
                slide_channel_partner_value_ago)) * 100)

        # Khóa học

        self._cr.execute('''select COUNT(id) from slide_slide WHERE Extract(MONTH FROM slide_slide.create_date) = Extract(MONTH FROM DATE(NOW()))
                AND Extract(Year FROM slide_slide.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_slide_value_moment = rec_ids_moment[0]

        self._cr.execute('''select COUNT(id) from slide_slide
                        WHERE date_trunc('month', DATE(slide_slide.create_date)) = date_trunc('month', DATE(NOW()) - interval '1 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_slide_value_ago = rec_ids_ago[0]

        if slide_slide_value_ago == 0:
            slide_slide_value_growth = slide_slide_value_moment * 100
        else:
            slide_slide_value_growth = (
                    ((slide_slide_value_moment - slide_slide_value_ago) / abs(slide_slide_value_ago)) * 100)

        # Kỳ thi

        self._cr.execute('''select COUNT(id) from survey_survey WHERE certification = true AND Extract(MONTH FROM survey_survey.create_date) = Extract(MONTH FROM DATE(NOW()))
            AND Extract(Year FROM survey_survey.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_exam_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_survey
                    WHERE certification = true AND date_trunc('month', DATE(survey_survey.create_date)) = date_trunc('month', DATE(NOW()) - interval '1 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_exam_value_ago = rec_ids_ago[0]

        if survey_exam_value_ago == 0:
            survey_exam_value_growth = survey_exam_value_moment * 100
        else:
            survey_exam_value_growth = (
                    ((survey_exam_value_moment - survey_exam_value_ago) / abs(survey_exam_value_ago)) * 100)

        # Bài khảo sát

        self._cr.execute(
            '''select COUNT(id) from survey_survey WHERE certification = false AND Extract(MONTH FROM survey_survey.create_date) = Extract(MONTH FROM DATE(NOW()))
            AND Extract(Year FROM survey_survey.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_survey_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_survey
                    WHERE certification = false AND date_trunc('month', DATE(survey_survey.create_date)) = date_trunc('month', DATE(NOW()) - interval '1 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_survey_value_ago = rec_ids_ago[0]

        if survey_survey_value_ago == 0:
            survey_survey_value_growth = survey_survey_value_moment * 100
        else:
            survey_survey_value_growth = (
                    ((survey_survey_value_moment - survey_survey_value_ago) / abs(survey_survey_value_ago)) * 100)

        # Câu hỏi

        self._cr.execute(
            '''select COUNT(id) from slide_question WHERE Extract(MONTH FROM slide_question.create_date) = Extract(MONTH FROM DATE(NOW()))
            AND Extract(Year FROM slide_question.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_question_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_question WHERE Extract(MONTH FROM survey_question.create_date) = Extract(MONTH FROM DATE(NOW()))
            AND Extract(Year FROM survey_question.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_question_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from slide_question
                    WHERE date_trunc('month', DATE(slide_question.create_date)) = date_trunc('month', DATE(NOW()) - interval '1 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_question_value_ago = rec_ids_ago[0]

        self._cr.execute(
            '''select COUNT(id) from survey_question
                    WHERE date_trunc('month', DATE(survey_question.create_date)) = date_trunc('month', DATE(NOW()) - interval '1 month')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_question_value_ago = rec_ids_ago[0]

        total_question_moment = survey_question_value_moment + slide_question_value_moment

        total_question_ago = survey_question_value_ago + slide_question_value_ago

        if total_question_ago == 0:
            total_question_growth = total_question_moment * 100
        else:
            total_question_growth = (
                    ((total_question_moment - total_question_ago) / abs(total_question_ago)) * 100)

        data_month = {
            # Tổng người dùng
            'record_total_user_moment': slide_channel_partner_value_moment,
            'record_total_user_ago': slide_channel_partner_value_ago,
            'record_total_user_growth': round(slide_channel_partner_value_growth, 2),
            # Khóa học
            'record_course_moment': slide_slide_value_moment,
            'record_course_ago': slide_slide_value_ago,
            'record_course_growth': round(slide_slide_value_growth, 2),
            # Kỳ thi
            'record_survey_exam_moment': survey_exam_value_moment,
            'record_survey_exam_ago': survey_exam_value_ago,
            'record_survey_exam_growth': round(survey_exam_value_growth, 2),
            # Bài khảo sát
            'record_survey_survey_moment': survey_survey_value_moment,
            'record_survey_survey_ago': survey_survey_value_ago,
            'record_survey_survey_growth': round(survey_survey_value_growth, 2),
            # Câu hỏi
            'record_total_question_moment': total_question_moment,
            'record_total_question_ago': total_question_ago,
            'record_total_question_growth': round(total_question_growth, 2),
        }
        return data_month

    @api.model
    def mate_elearning_this_week(self):
        # Tổng người dùng
        self._cr.execute('''select COUNT(id) from slide_channel_partner WHERE Extract(MONTH FROM slide_channel_partner.create_date) = Extract(MONTH FROM DATE(NOW()))
        AND Extract(Week FROM slide_channel_partner.create_date) = Extract(Week FROM DATE(NOW())) AND
        Extract(Year FROM slide_channel_partner.create_date) = Extract(Year FROM DATE(NOW()))''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_channel_partner_value_moment = rec_ids_moment[0]

        self._cr.execute('''select COUNT(id) from slide_channel_partner
                        WHERE date_trunc('week', DATE(slide_channel_partner.create_date)) = date_trunc('week', DATE(NOW()) - interval '1 week')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_channel_partner_value_ago = rec_ids_ago[0]

        if slide_channel_partner_value_ago == 0:
            slide_channel_partner_value_growth = slide_channel_partner_value_moment * 100
        else:
            slide_channel_partner_value_growth = (((
                                                           slide_channel_partner_value_moment - slide_channel_partner_value_ago) / abs(
                slide_channel_partner_value_ago)) * 100)

        # Khóa học

        self._cr.execute('''select COUNT(id) from slide_slide WHERE Extract(MONTH FROM slide_slide.create_date) = Extract(MONTH FROM DATE(NOW()))
                AND Extract(Week FROM slide_slide.create_date) = Extract(Week FROM DATE(NOW())) AND
                Extract(Year FROM slide_slide.create_date) = Extract(Year FROM DATE(NOW()))''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_slide_value_moment = rec_ids_moment[0]

        self._cr.execute('''select COUNT(id) from slide_slide
                                WHERE date_trunc('week', DATE(slide_slide.create_date)) = date_trunc('week', DATE(NOW()) - interval '1 week')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_slide_value_ago = rec_ids_ago[0]

        if slide_slide_value_ago == 0:
            slide_slide_value_growth = slide_slide_value_moment * 100
        else:
            slide_slide_value_growth = (
                    ((slide_slide_value_moment - slide_slide_value_ago) / abs(slide_slide_value_ago)) * 100)

        # Kỳ thi

        self._cr.execute('''select COUNT(id) from survey_survey WHERE certification = true AND Extract(MONTH FROM survey_survey.create_date) = Extract(MONTH FROM DATE(NOW()))
                AND Extract(Week FROM survey_survey.create_date) = Extract(Week FROM DATE(NOW())) AND
                Extract(Year FROM survey_survey.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_exam_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_survey
                                WHERE certification = true AND date_trunc('week', DATE(survey_survey.create_date)) = date_trunc('week', DATE(NOW()) - interval '1 week')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_exam_value_ago = rec_ids_ago[0]

        if survey_exam_value_ago == 0:
            survey_exam_value_growth = survey_exam_value_moment * 100
        else:
            survey_exam_value_growth = (
                    ((survey_exam_value_moment - survey_exam_value_ago) / abs(survey_exam_value_ago)) * 100)

        # Bài khảo sát

        self._cr.execute(
            '''select COUNT(id) from survey_survey WHERE certification = false AND Extract(MONTH FROM survey_survey.create_date) = Extract(MONTH FROM DATE(NOW()))
                AND Extract(Week FROM survey_survey.create_date) = Extract(Week FROM DATE(NOW())) AND
                Extract(Year FROM survey_survey.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_survey_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_survey
                                WHERE certification = false AND date_trunc('week', DATE(survey_survey.create_date)) = date_trunc('week', DATE(NOW()) - interval '1 week')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_survey_value_ago = rec_ids_ago[0]

        if survey_survey_value_ago == 0:
            survey_survey_value_growth = survey_survey_value_moment * 100
        else:
            survey_survey_value_growth = (
                    ((survey_survey_value_moment - survey_survey_value_ago) / abs(survey_survey_value_ago)) * 100)

        # Câu hỏi

        self._cr.execute(
            '''select COUNT(id) from slide_question WHERE Extract(MONTH FROM slide_question.create_date) = Extract(MONTH FROM DATE(NOW()))
                AND Extract(Week FROM slide_question.create_date) = Extract(Week FROM DATE(NOW())) AND
                Extract(Year FROM slide_question.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_question_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from survey_question WHERE Extract(MONTH FROM survey_question.create_date) = Extract(MONTH FROM DATE(NOW()))
                AND Extract(Week FROM survey_question.create_date) = Extract(Week FROM DATE(NOW())) AND
                Extract(Year FROM survey_question.create_date) = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_question_value_moment = rec_ids_moment[0]

        self._cr.execute(
            '''select COUNT(id) from slide_question
                                WHERE date_trunc('week', DATE(slide_question.create_date)) = date_trunc('week', DATE(NOW()) - interval '1 week')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        survey_question_value_ago = rec_ids_ago[0]

        self._cr.execute(
            '''select COUNT(id) from survey_question
                                WHERE date_trunc('week', DATE(survey_question.create_date)) = date_trunc('week', DATE(NOW()) - interval '1 week')''')
        record_ago = self._cr.dictfetchall()
        rec_ids_ago = [item['count'] for item in record_ago]
        slide_question_value_ago = rec_ids_ago[0]

        total_question_moment = survey_question_value_moment + slide_question_value_moment

        total_question_ago = survey_question_value_ago + slide_question_value_ago

        if total_question_ago == 0:
            total_question_growth = total_question_moment * 100
        else:
            total_question_growth = (
                    ((total_question_moment - total_question_ago) / abs(total_question_ago)) * 100)

        data_week = {
            # Tổng người dùng
            'record_total_user_moment': slide_channel_partner_value_moment,
            'record_total_user_ago': slide_channel_partner_value_ago,
            'record_total_user_growth': round(slide_channel_partner_value_growth, 2),
            # Khóa học
            'record_course_moment': slide_slide_value_moment,
            'record_course_ago': slide_slide_value_ago,
            'record_course_growth': round(slide_slide_value_growth, 2),
            # Kỳ thi
            'record_survey_exam_moment': survey_exam_value_moment,
            'record_survey_exam_ago': survey_exam_value_ago,
            'record_survey_exam_growth': round(survey_exam_value_growth, 2),
            # Bài khảo sát
            'record_survey_survey_moment': survey_survey_value_moment,
            'record_survey_survey_ago': survey_survey_value_ago,
            'record_survey_survey_growth': round(survey_survey_value_growth, 2),
            # Câu hỏi
            'record_total_question_moment': total_question_moment,
            'record_total_question_ago': total_question_ago,
            'record_total_question_growth': round(total_question_growth, 2),
        }
        return data_week

    @api.model
    def get_top_survey_exam_department(self):
        """Tỉ lệ phòng ban tham gia kỳ thi"""
        # HienTen
        self._cr.execute('''SELECT hr_employee.name FROM ((hr_employee
        full outer join hr_department ON hr_employee.department_id = hr_department.id)
        full outer join slide_channel_partner ON hr_employee.user_id = slide_channel_partner.partner_id)
        where hr_department.name = 'Sales' and hr_employee.name is not null
        order by hr_employee.name DESC limit 1''')

        data1 = self._cr.fetchall()
        top_survey_exam_name = []
        for rec in data1:
            rec_list = list(rec)
            top_survey_exam_name.append(rec_list)

        self._cr.execute('''SELECT hr_department.name FROM ((hr_employee
        full outer join hr_department ON hr_employee.department_id = hr_department.id)
        full outer join slide_channel_partner ON hr_employee.user_id = slide_channel_partner.partner_id)
        where hr_employee.name is not null
        order by hr_employee.name DESC limit 1''')

        data1 = self._cr.fetchall()
        top_survey_exam_job = []
        for rec in data1:
            rec_list = list(rec)
            top_survey_exam_job.append(rec_list)

        # Tỷ lệ
        # Tổng người dùng
        self._cr.execute('''select COUNT(id) from slide_channel_partner  WHERE Extract(Year FROM slide_channel_partner.create_date)
         = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        slide_channel_partner_value_moment = rec_ids_moment[0]

        # Kỳ thi
        self._cr.execute('''select COUNT(id) from survey_survey WHERE certification = true AND Extract(Year FROM survey_survey.create_date)
                         = Extract(Year FROM DATE(NOW()))''')
        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        survey_exam_value_moment = rec_ids_moment[0]

        top_survey_exam_percent = survey_exam_value_moment / slide_channel_partner_value_moment * 100

        return {'top_survey_exam_name': top_survey_exam_name,
                'top_survey_exam_job': top_survey_exam_job,
                'top_survey_exam_percent': round(top_survey_exam_percent, 2),
                }

    @api.model
    def get_top_course(self):
        """Top 5 khóa học có tỉ lệ tham gia nhiều nhất"""
        # Tên khóa học
        # Top 1
        self._cr.execute('''SELECT slide_channel.name FROM ((slide_channel
        inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,slide_channel.name
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 0''')
        data1 = self._cr.fetchall()

        get_top_course_name_top1 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_course_name_top1.append(rec_list)

        # Top 2
        self._cr.execute('''SELECT slide_channel.name FROM ((slide_channel
            inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
            group by slide_channel_partner.channel_id,slide_channel.name
            order by count(slide_channel_partner.channel_id) desc limit 1 offset 1''')
        data1 = self._cr.fetchall()

        get_top_course_name_top2 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_course_name_top2.append(rec_list)

        # Top 3
        self._cr.execute('''SELECT slide_channel.name FROM ((slide_channel
            inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
            group by slide_channel_partner.channel_id,slide_channel.name
            order by count(slide_channel_partner.channel_id) desc limit 1 offset 2''')
        data1 = self._cr.fetchall()

        get_top_course_name_top3 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_course_name_top3.append(rec_list)

        # Top 4
        self._cr.execute('''SELECT slide_channel.name FROM ((slide_channel
            inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
            group by slide_channel_partner.channel_id,slide_channel.name
            order by count(slide_channel_partner.channel_id) desc limit 1 offset 3''')
        data1 = self._cr.fetchall()

        get_top_course_name_top4 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_course_name_top4.append(rec_list)

        # Top 5
        self._cr.execute('''SELECT slide_channel.name FROM ((slide_channel
            inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
            group by slide_channel_partner.channel_id,slide_channel.name
            order by count(slide_channel_partner.channel_id) desc limit 1 offset 4''')
        data1 = self._cr.fetchall()

        get_top_course_name_top5 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_course_name_top5.append(rec_list)


        # channel_type
        # top1
        self._cr.execute('''SELECT slide_channel.channel_type FROM ((slide_channel
        inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,slide_channel.channel_type
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 0''')
        data1 = self._cr.fetchall()

        get_top_course_top1_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_course_top1_channel_type.append(rec_list)

        # top2
        self._cr.execute('''SELECT slide_channel.channel_type FROM ((slide_channel
            inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
            group by slide_channel_partner.channel_id,slide_channel.channel_type
            order by count(slide_channel_partner.channel_id) desc limit 1 offset 1''')
        data1 = self._cr.fetchall()

        get_top_course_top2_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_course_top2_channel_type.append(rec_list)

        # top3
        self._cr.execute('''SELECT slide_channel.channel_type FROM ((slide_channel
                inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
                group by slide_channel_partner.channel_id,slide_channel.channel_type
                order by count(slide_channel_partner.channel_id) desc limit 1 offset 2''')
        data1 = self._cr.fetchall()

        get_top_course_top3_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_course_top3_channel_type.append(rec_list)

        # top4
        self._cr.execute('''SELECT slide_channel.channel_type FROM ((slide_channel
                inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
                group by slide_channel_partner.channel_id,slide_channel.channel_type
                order by count(slide_channel_partner.channel_id) desc limit 1 offset 3''')
        data1 = self._cr.fetchall()

        get_top_course_top4_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_course_top4_channel_type.append(rec_list)

        # top5
        self._cr.execute('''SELECT slide_channel.channel_type FROM ((slide_channel
                inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
                group by slide_channel_partner.channel_id,slide_channel.channel_type
                order by count(slide_channel_partner.channel_id) desc limit 1 offset 4''')
        data1 = self._cr.fetchall()

        get_top_course_top5_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_course_top5_channel_type.append(rec_list)

        #Tỉ lệ
        # Top1
        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((slide_channel
        inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 0''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_course_percent_top1 = rec_ids_moment[0]

        # Top2
        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((slide_channel
                inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
                group by slide_channel_partner.channel_id
                order by count(slide_channel_partner.channel_id) desc limit 1 offset 1''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_course_percent_top2 = rec_ids_moment[0]

        # Top3
        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((slide_channel
                inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
                group by slide_channel_partner.channel_id
                order by count(slide_channel_partner.channel_id) desc limit 1 offset 2''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_course_percent_top3 = rec_ids_moment[0]

        # Top4
        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((slide_channel
                inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
                group by slide_channel_partner.channel_id
                order by count(slide_channel_partner.channel_id) desc limit 1 offset 3''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_course_percent_top4 = rec_ids_moment[0]

        # Top5
        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((slide_channel
                inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))
                group by slide_channel_partner.channel_id
                order by count(slide_channel_partner.channel_id) desc limit 1 offset 4''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_course_percent_top5 = rec_ids_moment[0]


        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((slide_channel
        inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_course_total_percent = rec_ids_moment[0]

        course_percentage_top1 = (get_top_course_percent_top1 / get_top_course_total_percent * 100)

        course_percentage_top2 = (get_top_course_percent_top2 / get_top_course_total_percent * 100)

        course_percentage_top3 = (get_top_course_percent_top3 / get_top_course_total_percent * 100)

        course_percentage_top4 = (get_top_course_percent_top4 / get_top_course_total_percent * 100)

        course_percentage_top5 = (get_top_course_percent_top5 / get_top_course_total_percent * 100)

        return {'get_top_course_name_top1': get_top_course_name_top1,
                'get_top_course_name_top2': get_top_course_name_top2,
                'get_top_course_name_top3': get_top_course_name_top3,
                'get_top_course_name_top4': get_top_course_name_top4,
                'get_top_course_name_top5': get_top_course_name_top5,
                'get_top_course_top1_channel_type': get_top_course_top1_channel_type,
                'get_top_course_top2_channel_type': get_top_course_top2_channel_type,
                'get_top_course_top3_channel_type': get_top_course_top3_channel_type,
                'get_top_course_top4_channel_type': get_top_course_top4_channel_type,
                'get_top_course_top5_channel_type': get_top_course_top5_channel_type,
                'course_percentage_top1': round(course_percentage_top1, 0),
                'course_percentage_top2': round(course_percentage_top2, 0),
                'course_percentage_top3': round(course_percentage_top3, 0),
                'course_percentage_top4': round(course_percentage_top4, 0),
                'course_percentage_top5': round(course_percentage_top5, 0),

        }

    @api.model
    def get_top_survey_exam(self):
        """Top 5 kỳ thi có tỉ lệ tham gia nhiều nhất"""
        # Tên kỳ thi
        # Top 1
        self._cr.execute('''SELECT survey_survey.title FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,survey_survey.title
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 0''')
        data1 = self._cr.fetchall()

        get_top_survey_exam_name_top1 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_exam_name_top1.append(rec_list)

        # Top 2
        self._cr.execute('''SELECT survey_survey.title FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,survey_survey.title
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 1''')
        data1 = self._cr.fetchall()

        get_top_survey_exam_name_top2 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_exam_name_top2.append(rec_list)

        # Top 3
        self._cr.execute('''SELECT survey_survey.title FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,survey_survey.title
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 2''')
        data1 = self._cr.fetchall()

        get_top_survey_exam_name_top3 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_exam_name_top3.append(rec_list)

        # Top 4
        self._cr.execute('''SELECT survey_survey.title FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,survey_survey.title
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 3''')
        data1 = self._cr.fetchall()

        get_top_survey_exam_name_top4 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_exam_name_top4.append(rec_list)

        # Top 5
        self._cr.execute('''SELECT survey_survey.title FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,survey_survey.title
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 4''')
        data1 = self._cr.fetchall()

        get_top_survey_exam_name_top5 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_exam_name_top5.append(rec_list)


        # channel_type
        # top1
        self._cr.execute('''SELECT survey_survey.questions_layout FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,survey_survey.questions_layout
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 0''')
        data1 = self._cr.fetchall()

        get_top_survey_exam_top1_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_exam_top1_channel_type.append(rec_list)

        # top2
        self._cr.execute('''SELECT survey_survey.questions_layout FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,survey_survey.questions_layout
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 1''')
        data1 = self._cr.fetchall()

        get_top_survey_exam_top2_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_exam_top2_channel_type.append(rec_list)

        # top3
        self._cr.execute('''SELECT survey_survey.questions_layout FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,survey_survey.questions_layout
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 2''')
        data1 = self._cr.fetchall()

        get_top_survey_exam_top3_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_exam_top3_channel_type.append(rec_list)

        # top4
        self._cr.execute('''SELECT survey_survey.questions_layout FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,survey_survey.questions_layout
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 3''')
        data1 = self._cr.fetchall()

        get_top_survey_exam_top4_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_exam_top4_channel_type.append(rec_list)

        # top5
        self._cr.execute('''SELECT survey_survey.questions_layout FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id,survey_survey.questions_layout
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 4''')
        data1 = self._cr.fetchall()

        get_top_survey_exam_top5_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_exam_top5_channel_type.append(rec_list)

        #Tỉ lệ
        # Top1
        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 0''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_survey_exam_percent_top1 = rec_ids_moment[0]

        # Top2
        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 1''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_survey_exam_percent_top2 = rec_ids_moment[0]

        # Top3
        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 2''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_survey_exam_percent_top3 = rec_ids_moment[0]

        # Top4
        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 3''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_survey_exam_percent_top4 = rec_ids_moment[0]

        # Top5
        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((survey_survey
        inner join slide_channel_partner ON survey_survey.id = slide_channel_partner.channel_id))
        group by slide_channel_partner.channel_id
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 4''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_survey_exam_percent_top5 = rec_ids_moment[0]


        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((slide_channel
        inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_survey_exam_total_percent = rec_ids_moment[0]

        survey_exam_percentage_top1 = (get_top_survey_exam_percent_top1 / get_top_survey_exam_total_percent * 100)

        survey_exam_percentage_top2 = (get_top_survey_exam_percent_top2 / get_top_survey_exam_total_percent * 100)

        survey_exam_percentage_top3 = (get_top_survey_exam_percent_top3 / get_top_survey_exam_total_percent * 100)

        survey_exam_percentage_top4 = (get_top_survey_exam_percent_top4 / get_top_survey_exam_total_percent * 100)

        survey_exam_percentage_top5 = (get_top_survey_exam_percent_top5 / get_top_survey_exam_total_percent * 100)

        return {'get_top_survey_exam_name_top1': get_top_survey_exam_name_top1,
                'get_top_survey_exam_name_top2': get_top_survey_exam_name_top2,
                'get_top_survey_exam_name_top3': get_top_survey_exam_name_top3,
                'get_top_survey_exam_name_top4': get_top_survey_exam_name_top4,
                'get_top_survey_exam_name_top5': get_top_survey_exam_name_top5,
                'get_top_survey_exam_top1_channel_type': get_top_survey_exam_top1_channel_type,
                'get_top_survey_exam_top2_channel_type': get_top_survey_exam_top2_channel_type,
                'get_top_survey_exam_top3_channel_type': get_top_survey_exam_top3_channel_type,
                'get_top_survey_exam_top4_channel_type': get_top_survey_exam_top4_channel_type,
                'get_top_survey_exam_top5_channel_type': get_top_survey_exam_top5_channel_type,
                'survey_exam_percentage_top1': round(survey_exam_percentage_top1, 0),
                'survey_exam_percentage_top2': round(survey_exam_percentage_top2, 0),
                'survey_exam_percentage_top3': round(survey_exam_percentage_top3, 0),
                'survey_exam_percentage_top4': round(survey_exam_percentage_top4, 0),
                'survey_exam_percentage_top5': round(survey_exam_percentage_top5, 0),

        }

    @api.model
    def get_top_survey_user(self):
        """Top 5 bài khảo sát có tỉ lệ tham gia nhiều nhất"""
        # Tên bài khảo sát
        # Top 1
        self._cr.execute('''SELECT survey_user_input.email FROM ((survey_user_input
        inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        group by slide_channel_partner.partner_id,survey_user_input.email
        order by count(slide_channel_partner.partner_id) desc limit 1 offset 0''')
        data1 = self._cr.fetchall()

        get_top_survey_user_input_name_top1 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_user_input_name_top1.append(rec_list)

        # Top 2
        self._cr.execute('''SELECT survey_user_input.email FROM ((survey_user_input
        inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        group by slide_channel_partner.partner_id,survey_user_input.email
        order by count(slide_channel_partner.partner_id) desc limit 1 offset 1''')
        data1 = self._cr.fetchall()

        get_top_survey_user_input_name_top2 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_user_input_name_top2.append(rec_list)

        # Top 3
        self._cr.execute('''SELECT survey_user_input.email FROM ((survey_user_input
        inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        group by slide_channel_partner.partner_id,survey_user_input.email
        order by count(slide_channel_partner.partner_id) desc limit 1 offset 2''')
        data1 = self._cr.fetchall()

        get_top_survey_user_input_name_top3 = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_user_input_name_top3.append(rec_list)

        # # Top 4
        # self._cr.execute('''SELECT survey_user_input.email FROM ((survey_user_input
        # inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        # group by slide_channel_partner.partner_id,survey_user_input.email
        # order by slide_channel_partner.partner_id asc limit 1 offset 3''')
        # data1 = self._cr.fetchall()
        #
        # get_top_survey_user_input_name_top4 = []
        # for rec in data1:
        #     rec_list = list(rec)
        #     get_top_survey_user_input_name_top4.append(rec_list)

        # # Top 5
        # self._cr.execute('''SELECT survey_user_input.email FROM ((survey_user_input
        # inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        # group by slide_channel_partner.partner_id,survey_user_input.email
        # order by slide_channel_partner.partner_id asc limit 1 offset 4''')
        # data1 = self._cr.fetchall()
        #
        # get_top_survey_user_input_name_top5 = []
        # for rec in data1:
        #     rec_list = list(rec)
        #     get_top_survey_user_input_name_top5.append(rec_list)

        # channel_type
        # top1
        self._cr.execute('''SELECT survey_user_input.state FROM ((survey_user_input
        inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        group by slide_channel_partner.channel_id,survey_user_input.state
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 0''')
        data1 = self._cr.fetchall()

        get_top_survey_user_input_top1_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_user_input_top1_channel_type.append(rec_list)

        # top2
        self._cr.execute('''SELECT survey_user_input.state FROM ((survey_user_input
        inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        group by slide_channel_partner.channel_id,survey_user_input.state
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 1''')
        data1 = self._cr.fetchall()

        get_top_survey_user_input_top2_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_user_input_top2_channel_type.append(rec_list)

        # top3
        self._cr.execute('''SELECT survey_user_input.state FROM ((survey_user_input
        inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        group by slide_channel_partner.channel_id,survey_user_input.state
        order by count(slide_channel_partner.channel_id) desc limit 1 offset 2''')
        data1 = self._cr.fetchall()

        get_top_survey_user_input_top3_channel_type = []
        for rec in data1:
            rec_list = list(rec)
            get_top_survey_user_input_top3_channel_type.append(rec_list)

        # # top4
        # self._cr.execute('''SELECT survey_user_input.state FROM ((survey_user_input
        # inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        # group by slide_channel_partner.channel_id,survey_user_input.state
        # order by slide_channel_partner.channel_id asc limit 1 offset 3''')
        # data1 = self._cr.fetchall()
        #
        # get_top_survey_user_input_top4_channel_type = []
        # for rec in data1:
        #     rec_list = list(rec)
        #     get_top_survey_user_input_top4_channel_type.append(rec_list)
        #
        # # top5
        # self._cr.execute('''SELECT survey_user_input.state FROM ((survey_user_input
        # inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        # group by slide_channel_partner.channel_id,survey_user_input.state
        # order by slide_channel_partner.channel_id asc limit 1 offset 4''')
        # data1 = self._cr.fetchall()
        #
        # get_top_survey_user_input_top5_channel_type = []
        # for rec in data1:
        #     rec_list = list(rec)
        #     get_top_survey_user_input_top5_channel_type.append(rec_list)
        #
        # Tỉ lệ
        # Top1
        self._cr.execute('''SELECT count(survey_user_input.id) FROM ((survey_user_input
        inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        group by slide_channel_partner.partner_id
        order by count(slide_channel_partner.partner_id) desc limit 1 offset 0''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_survey_user_input_percent_top1 = rec_ids_moment[0]

        # Top2
        self._cr.execute('''SELECT count(survey_user_input.id) FROM ((survey_user_input
        inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        group by slide_channel_partner.partner_id
        order by count(slide_channel_partner.partner_id) desc limit 1 offset 1''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_survey_user_input_percent_top2 = rec_ids_moment[0]

        # Top3
        self._cr.execute('''SELECT count(survey_user_input.id) FROM ((survey_user_input
        inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        group by slide_channel_partner.partner_id
        order by count(slide_channel_partner.partner_id) desc limit 1 offset 2''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_survey_user_input_percent_top3 = rec_ids_moment[0]

        # # Top4
        # self._cr.execute('''SELECT count(survey_user_input.partner_id) FROM ((survey_user_input
        # inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        # group by slide_channel_partner.partner_id
        # order by slide_channel_partner.partner_id asc limit 1 offset 3''')
        #
        # record_moment = self._cr.dictfetchall()
        # rec_ids_moment = [item['count'] for item in record_moment]
        # get_top_survey_user_input_percent_top4 = rec_ids_moment[0]
        #
        # # Top5
        # self._cr.execute('''SELECT count(survey_user_input.partner_id) FROM ((survey_user_input
        # inner join slide_channel_partner ON survey_user_input.id = slide_channel_partner.partner_id))
        # group by slide_channel_partner.partner_id
        # order by slide_channel_partner.partner_id asc limit 1 offset 4''')
        #
        # record_moment = self._cr.dictfetchall()
        # rec_ids_moment = [item['count'] for item in record_moment]
        # get_top_survey_user_input_percent_top5 = rec_ids_moment[0]

        self._cr.execute('''SELECT count(slide_channel_partner.channel_id) FROM ((slide_channel
        inner join slide_channel_partner ON slide_channel.id = slide_channel_partner.channel_id))''')

        record_moment = self._cr.dictfetchall()
        rec_ids_moment = [item['count'] for item in record_moment]
        get_top_survey_user_input_total_percent = rec_ids_moment[0]

        if get_top_survey_user_input_percent_top1 == 0:
            survey_user_input_percentage_top1 = 0
        else:
            survey_user_input_percentage_top1 = (get_top_survey_user_input_percent_top1 / get_top_survey_user_input_total_percent * 100)

        if get_top_survey_user_input_percent_top2 == 0:
            survey_user_input_percentage_top2 = 0
        else:
            survey_user_input_percentage_top2 = (
                        get_top_survey_user_input_percent_top2 / get_top_survey_user_input_total_percent * 100)

        if get_top_survey_user_input_percent_top3 == 0:
            survey_user_input_percentage_top3 = 0
        else:
            survey_user_input_percentage_top3 = (get_top_survey_user_input_percent_top3 / get_top_survey_user_input_total_percent * 100)

        # if get_top_survey_user_input_percent_top4 == 0:
        #     survey_user_input_percentage_top4 = 0
        # else:
        #     survey_user_input_percentage_top4 = (get_top_survey_user_input_percent_top4 / get_top_survey_user_input_total_percent * 100)
        #
        # if get_top_survey_user_input_percent_top5 == 0:
        #     survey_user_input_percentage_top5 = 0
        # else:
        #     survey_user_input_percentage_top5 = (get_top_survey_user_input_percent_top5 / get_top_survey_user_input_total_percent * 100)


        return {'get_top_survey_user_input_name_top1': get_top_survey_user_input_name_top1,
                'get_top_survey_user_input_name_top2': get_top_survey_user_input_name_top2,
                'get_top_survey_user_input_name_top3': get_top_survey_user_input_name_top3,
                # 'get_top_survey_user_input_name_top4': get_top_survey_user_input_name_top4,
                # 'get_top_survey_user_input_name_top5': get_top_survey_user_input_name_top5,
                'get_top_survey_user_input_top1_channel_type': get_top_survey_user_input_top1_channel_type,
                'get_top_survey_user_input_top2_channel_type': get_top_survey_user_input_top2_channel_type,
                'get_top_survey_user_input_top3_channel_type': get_top_survey_user_input_top3_channel_type,
                # 'get_top_survey_user_input_top4_channel_type': get_top_survey_user_input_top4_channel_type,
                # 'get_top_survey_user_input_top5_channel_type': get_top_survey_user_input_top5_channel_type,
                'survey_user_input_percentage_top1': round(survey_user_input_percentage_top1, 0),
                'survey_user_input_percentage_top2': round(survey_user_input_percentage_top2, 0),
                'survey_user_input_percentage_top3': round(survey_user_input_percentage_top3, 0),
                # 'survey_user_input_percentage_top4': round(survey_user_input_percentage_top4, 0),
                # 'survey_user_input_percentage_top5': round(survey_user_input_percentage_top5, 0),
                }
