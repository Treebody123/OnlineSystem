from django.contrib import admin
from .models import EntryNOC,UserFullName
from django.contrib.auth.models import Group,User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.urls import path
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q


NOC_add_fieldsets = (
        ('Recommended fields',{
            'fields':('rep_date','finding_source','ticket_num','finding_description')
        }),
        ('Other options',{
            'classes':('collapse',),
            'fields': (
                'finding_level', 'finding_responsible','quality_track_measurement',
                'finding_final_status'
            )
        }),
	)

NOC_change_fieldsets = (
        ('Recommended fields',{
            'fields':('rep_date','finding_source','ticket_num','finding_description')
        }),
        ('Other options',{
            'classes':('collapse',),
            'fields': (
                'finding_level', 'finding_responsible','quality_track_measurement',
                'acknowledge_status','email_send',
                'quality_track_comments','finding_final_status',
            )
        }),
	)



# Register your models here.


admin.site.site_header = 'Quality Online Track Management System'
admin.site.site_title = 'Quality Online System'
admin.site.index_title = 'Quality Management'

@admin.register(EntryNOC)
class EntryNOCAdmin(admin.ModelAdmin):
    list_display = ('ticket_num','rep_date','finding_description','finding_responsible','acknowledge_status','finding_final_status','Colored_status')
    search_fields = ('ticket_num','finding_description')
    #list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20
    admin.site.empty_value_display = '--------'
    date_hierarchy = 'rep_date'
    ordering = ('-rep_date',)



    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if  request.user.is_superuser :                    #判断是否是admin
            return qs
        elif Group.objects.get(user=request.user).name == 'NOC_Management':      #判断当前用户是否属于NOC_Management组
            return qs
        elif Group.objects.get(user=request.user).name == 'NOC_OSN_Management':
            return qs
        return qs.filter(finding_responsible=request.user)

    def get_readonly_fields(self,request,obj=None):
        self.readonly_fields = []
        # if request.user.is_superuser :
        #     self.readonly_fields = []
        if Group.objects.get(user=request.user).name == 'NOC_Management':
            self.readonly_fields = ['quality_track_comments']
        elif Group.objects.get(user=request.user).name == 'NOC_Group_Members':
            self.readonly_fields = ['ticket_num','rep_date','finding_responsible','finding_source','finding_description','finding_level','quality_track_measurement','finding_final_status']
        return self.readonly_fields

    def get_actions(self, request):
        actions = super().get_actions(request)
#        if not request.user.is_superuser :
        if Group.objects.get(user=request.user).name == 'NOC_Group_Members' or Group.objects.get(user=request.user).name == 'NOC_OSN_Management':
            del actions['delete_selected']
        return actions

    def get_list_filter(self,request):
        if Group.objects.get(user=request.user).name == 'NOC_Group_Members':
            self.list_filter = ['finding_final_status', 'finding_level']
        # elif request.user.is_superuser:
        #     self.list_filter = ['finding_final_status','finding_level','finding_responsible']
        elif Group.objects.get(user=request.user).name == 'NOC_Management':
            self.list_filter = ['finding_final_status', 'finding_level', 'finding_responsible']
        elif Group.objects.get(user=request.user).name == 'NOC_OSN_Management':
            self.list_filter = ['finding_final_status']
        return self.list_filter


    def send_email(self,request,to_email,mail_msg):
        email_host = 'rb-smtp-int.bosch.com'
        from_email = 'Yu.liu7@cn.bosch.com'

        msg = MIMEMultipart()
        msg['Subject'] = 'Notification to Quality finding'  # 标题
        msg['From'] = from_email  # 邮件显示发件人地址
        msg['To'] = to_email  # needs to debug
#        msg['To'] = 'Yu.liu7@cn.bosch.com,Yu.liu7@cn.bosch.com'      this is working

        msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))

        smtp = smtplib.SMTP()
        smtp.connect(email_host, 25)
        smtp.sendmail(from_email, to_email, msg.as_string())
        smtp.quit()

    def save_model(self,request,obj,form,change):
        if change:           #页面修改时
            if obj.email_send:
                if Group.objects.get(user=request.user).name == 'NOC_Group_Members':
                    to_email_userlist = User.objects.filter(groups__name='NOC_Management')         #send mail to person in group " NOC Management"
                    to_email = []
                    for i in to_email_userlist:
                        to_email.append(i.email)
                    mail_msg = 'Please notes that {} has updated Quality issue　{}'.format(obj.finding_responsible,obj.ticket_num)
                    mail_msg += '''
                    <p><a href="http://127.0.0.1:8000:"> visit Quality Track System</a></p>
                    '''
                    self.send_email(request,to_email,mail_msg)
                elif Group.objects.get(user=request.user).name == 'NOC_Management':   #send mail function to NOC responsible
                    to_email_firstname = obj.finding_responsible.first_name
                    to_email_lastname = obj.finding_responsible.last_name
                    to_email = UserFullName.objects.get(first_name=to_email_firstname,
                                                        last_name=to_email_lastname).email
                    mail_msg = 'Please notes that your Quality issue {} has been updated.'.format(
                        obj.ticket_num)
                    mail_msg += '''
                            <p><a href="http://127.0.0.1:8000:"> visit Quality Track System</a></p>
                            '''
                    self.send_email(request, to_email, mail_msg)


        else:       #新增加quality finding时
            if Group.objects.get(user=request.user).name == 'NOC_Management':
                if (obj.finding_responsible != None)  and (obj.finding_final_status == 'A' or obj.finding_final_status == '-') :
                    to_email_firstname = obj.finding_responsible.first_name
                    to_email_lastname = obj.finding_responsible.last_name
                    to_email = UserFullName.objects.get(first_name=to_email_firstname,last_name=to_email_lastname).email
                    mail_msg = 'Please notes that You have been assigned one new Quality issue {}'.format(obj.ticket_num)
                    mail_msg += '''
                    <p><a href="http://127.0.0.1:8000:"> visit Quality Track System</a></p>
                    '''
                    self.send_email(request, to_email, mail_msg)
            elif Group.objects.get(user=request.user).name == 'NOC_OSN_Management':     #OSN新增quality issue时, 邮件通知NOC management
                NOC_management_person = User.objects.filter(groups__name='NOC_Management')
                to_email = []
                for i in NOC_management_person:
                    to_email.append(i.email)
                mail_msg = 'Please note OSN has added one new Quality issue {}'.format(obj.ticket_num)
                mail_msg += '''
                <p><a href="http://127.0.0.1:8000:"> visit Quality Track System</a></p>
                '''
                self.send_email(request, to_email, mail_msg)
        super().save_model(request, obj, form, change)

    def add_view(self, request, form_url='', extra_context=None):
        self.fieldsets = NOC_add_fieldsets
        return self.changeform_view(request, None, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fieldsets = NOC_change_fieldsets
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('report/',self.my_view,name='report'),
            path('showdata/',self.show_data,name='show_data'),
        ]
        return my_urls + urls

    def my_view(self,request,obj=None):
        opts = self.model._meta
        app_label = opts.app_label

        content_name = 'Report'
        site_title =  admin.site.site_title
        site_header = admin.site.site_header
        site_url = admin.site.site_url
        context = {
            'site_title' : site_title,
            'site_header':site_header,
            'site_url':site_url,
            'content_name':content_name,
            'has_change_permission': self.has_change_permission(request, obj),
            'has_add_permission': self.has_add_permission(request),
            'has_permission': super().get_model_perms(request),
            'opts':opts,
            'app_label': app_label,
        }
        return render(request, 'admin/report.html',context=context)

    def get_entrynoc_top5_list(self,year,month):
        entrynoc_top5_list = []
        for i in range(1,month+1):
            wrong_ownergroup_num = EntryNOC.objects.filter(rep_date__year=year, rep_date__month=i,
                                                           finding_description__icontains='owner group').count()
            wrong_summary_resolution_description_num = EntryNOC.objects.filter(Q(rep_date__year=year),
                                                                            Q(rep_date__month=i),
                                                                            Q(finding_description__icontains='summary')|Q(finding_description__icontains='resolution description')
                                                                            ).count()
            wrong_incidenttype_num = EntryNOC.objects.filter(rep_date__year=year, rep_date__month=i,
                                                             finding_description__icontains='incident type').count()
            wrong_SLA_num = EntryNOC.objects.filter(rep_date__year=year, rep_date__month=i,
                                                    finding_description__icontains='SLA').count()
            wrong_CI_service_num = EntryNOC.objects.filter(Q(rep_date__year=year),
                                                        Q(rep_date__month=i),
                                                        Q(finding_description__icontains='CI+')|Q(finding_description__icontains='SERVICE+')
                                                        ).count()
            wrong_resolution_categorization_num = EntryNOC.objects.filter(rep_date__year=year, rep_date__month=i,
                                                   finding_description__icontains='resolution categorization').count()
            wrong_CI_unavailability_num =  EntryNOC.objects.filter(rep_date__year=year, rep_date__month=i,
                                                   finding_description__icontains='CI unavailability').count()

            wrong_impact_urgency_priority_num = EntryNOC.objects.filter(Q(rep_date__year=year),
                                                                     Q(rep_date__month=i),
                                                                     Q(finding_description__icontains='impact')|Q(finding_description__icontains='urgency')|Q(finding_description__icontains='priority')
                                                                     ).count()
            list1 = {'wrong owner group': wrong_ownergroup_num,
                     'wrong summary/resolution description': wrong_summary_resolution_description_num,
                     'wrong incident type': wrong_incidenttype_num,
                     'wrong SLA information': wrong_SLA_num,
                     'wrong CI+/SERVICE+': wrong_CI_service_num,
                     'wrong Impact/urgency/ticket priority':wrong_impact_urgency_priority_num,
                     'wrong CI unavailability':wrong_CI_unavailability_num,
                     'wrong Resolution categorization':wrong_resolution_categorization_num,
                     }
            top5_list_sorted = sorted(list1.items(), key=lambda x: x[1], reverse=True)[:5]  #数据结构[('wrong SLA information', 6), ('wrong incident type', 5), ('wrong owner group', 4), ('wrong CI+', 4), ('wrong summary', 3)]
            entrynoc_top5_list.append(top5_list_sorted)
        return entrynoc_top5_list


    @csrf_exempt
    def show_data(self,request,obj=None):
        if request.method == 'POST':
            year = request.POST.get("year")
            # cur_year = datetime.datetime.now().year
            # cur_month = datetime.datetime.now().month
            month_list = []
            num_list = []
            # entrynoc_top5_year = []
            # if int(year) < cur_year:
            #     entrynoc_top5_year = self.get_entrynoc_top5_list(year,12)
            #     for i in range(1,13):
            #         month_list.append(year+'.'+str(i))
            #         num_list.append(EntryNOC.objects.filter(rep_date__year=year,rep_date__month=i).count())
            # elif int(year) == cur_year:
            #     entrynoc_top5_year = self.get_entrynoc_top5_list(year, cur_month)
            #     for i in range(1,cur_month+1):
            entrynoc_top5_year = self.get_entrynoc_top5_list(year, 12)   #获取某一年所有月份的top5的多维list
            print(entrynoc_top5_year)
            for i in range(1,13):
                month_list.append(year + '.' + str(i))
                num_list.append(EntryNOC.objects.filter(rep_date__year=year, rep_date__month=i).count())
            context = {
                'month_list':json.dumps(month_list),
                'num_list':json.dumps(num_list),
                'entrynoc_top5_year':json.dumps(entrynoc_top5_year),
            }
            return render(request,'admin/test2.html',context=context)














