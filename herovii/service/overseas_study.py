# -*- coding: utf-8 -*-
from flask import json
from sqlalchemy import func
from herovii import db
from herovii.libs.error_code import NotFound
from herovii.models.InformationFlow.information_flow_banner import InformationFlowBanner
from herovii.models.org.teaching_course_enroll import TeachingCourseEnroll
from herovii.models.overseas.country import Country
from herovii.models.overseas.organization_to_university import OrganizationToUniversity
from herovii.models.overseas.university import University
from herovii.models.overseas.university_major import UniversityMajor

__author__ = 'yangchujie'


def get_overseas_study_banner_service(page, per_page):
    banner_count = db.session.query(InformationFlowBanner).filter(InformationFlowBanner.status == 1,
                                                                  InformationFlowBanner.show_pos == 3).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    banner_list = db.session.query(InformationFlowBanner) \
        .filter(InformationFlowBanner.status == 1,
                InformationFlowBanner.show_pos == 3) \
        .slice(start, stop) \
        .all()
    if banner_list:
        for banner in banner_list:
            jump_type = banner.jump_type
            banner_object = {
                'id': banner.id,
                'pic_url': banner.pic_url,
                'jump_type': jump_type,
                'url': banner.url
            }
            if jump_type == 2:
                post_id = banner.url
                banner_object['url'] = 'hisihi://post/detailinfo?id=' + post_id
            elif jump_type == 3:
                course_id = banner.url
                banner_object['url'] = 'hisihi://course/detailinfo?id=' + course_id
            elif jump_type == 4:
                org_id = banner.url
                banner_object['url'] = 'hisihi://organization/detailinfo?id=' + org_id
            elif jump_type == 5:
                university_id = banner.url
                banner_object['url'] = 'hisihi://university/detailinfo?id=' + university_id
            data_list.append(banner_object)
    return banner_count, data_list


def get_overseas_study_hot_country_service(page, per_page):
    country_count = db.session.query(Country).filter(Country.status == 1,
                                                     Country.is_hot == 1).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    country_list = db.session.query(Country.id, Country.name, Country.logo_url) \
        .filter(Country.status == 1,
                Country.is_hot == 1) \
        .order_by(Country.create_time.desc()) \
        .slice(start, stop) \
        .all()
    for country in country_list:
        data = {
            'id': country.id,
            'name': country.name,
            'logo_url': country.logo_url
        }
        data_list.append(data)
    return country_count, data_list


def get_overseas_study_hot_university_service(page, per_page):
    university_count = db.session.query(University).filter(University.status == 1,
                                                           University.is_hot == 1).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    university_list = db.session.query(University.id, University.name, University.logo_url) \
        .filter(University.status == 1,
                University.is_hot == 1) \
        .order_by(University.create_time.desc()) \
        .slice(start, stop) \
        .all()
    for university in university_list:
        data = {
            'id': university.id,
            'name': university.name,
            'logo_url': university.logo_url
        }
        data_list.append(data)
    return university_count, data_list


def get_overseas_study_university_info_service(uid):
    university = University.query.get(uid)
    if not university:
        raise NotFound(error_code=5008, error='大学信息不存在')
    graduate_majors_array = university.graduate_majors.split("#")
    undergraduate_majors_array = university.undergraduate_majors.split("#")
    graduate_major_text = []
    undergraduate_major_text = []
    for graduate_major_id in graduate_majors_array:
        major_info = UniversityMajor.query.get(graduate_major_id)
        if major_info:
            graduate_major_text.append(major_info.name)
    for undergraduate_major_id in undergraduate_majors_array:
        major_info = UniversityMajor.query.get(undergraduate_major_id)
        if major_info:
            undergraduate_major_text.append(major_info.name)
    return {
        'name': university.name,
        'website': university.website,
        'logo_url': university.logo_url,
        'undergraduate_major': undergraduate_major_text,
        'graduate_major': graduate_major_text,
        'introduction': university.introduction,
        'sia_recommend_level': university.sia_recommend_level,
        'sia_student_enrollment_rate': university.sia_student_enrollment_rate,
        'difficulty_of_application': university.difficulty_of_application,
        'tuition_fees': university.tuition_fees,
        'toefl': university.toefl,
        'ielts': university.ielts,
        'proportion_of_undergraduates': university.proportion_of_undergraduates,
        'scholarship': university.scholarship,
        'deadline_for_applications': university.deadline_for_applications,
        'application_requirements': university.application_requirements,
        'school_environment': university.school_environment
    }


def get_overseas_study_university_list_by_country_id_service(cid, page, per_page):
    university_count = db.session.query(University).filter(University.status == 1,
                                                           University.country_id == cid).count()
    data_list = []
    start = (page - 1) * per_page
    stop = start + per_page
    university_list = db.session.query(University.id, University.name, University.logo_url) \
        .filter(University.status == 1,
                University.country_id == cid) \
        .order_by(University.create_time.desc()) \
        .slice(start, stop) \
        .all()
    for university in university_list:
        organization_total_count = db.session.query(OrganizationToUniversity).filter(
            OrganizationToUniversity.status == 1,
            OrganizationToUniversity.teaching_course_id == 0,
            OrganizationToUniversity.university_id == university.id).count()
        teaching_course_list = db.session.query(OrganizationToUniversity) \
            .filter(OrganizationToUniversity.status == 1,
                    OrganizationToUniversity.teaching_course_id != 0,
                    OrganizationToUniversity.university_id == university.id) \
            .all()
        if len(teaching_course_list) == 0:
            enroll_total_count = 0
        else:
            teaching_course_id_list = []
            for teaching_course in teaching_course_list:
                teaching_course_id_list.append(str(teaching_course.teaching_course_id))
            enroll_total_count = db.session.query(TeachingCourseEnroll) \
                .filter(TeachingCourseEnroll.status == 1,
                        func.find_in_set(TeachingCourseEnroll.course_id, ','.join(teaching_course_id_list))) \
                .count()
        data = {
            'id': university.id,
            'name': university.name,
            'logo_url': university.logo_url,
            'organization_total_count': organization_total_count,
            'enroll_total_count': enroll_total_count
        }
        data_list.append(data)
    return university_count, data_list
