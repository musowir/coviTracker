from django.db import models
from django.contrib.auth.models import User


STATE_LIST = (
        ("01", "Jammu and Kashmir"),
        ("02", "Himachal Pradesh"),
        ("03", "Punjab"),
        ("04", "Chattisgarh"),
        ("05", "UTTARAKHAND"),
        ("06", "Haryana"),
        ("07", "DELHI"),
        ("08", "Rajasthan"),
        ("09", "Uttar Pradesh"),
        ("10", "Bihar"),
        ("11", "Sikkim"),
        ("12", "Arunachal Pradesh"),
        ("13", "Nagaland"),
        ("14", "Manipur"),
        ("15", "MIZORAM"),
        ("16", "TRIPURA"),
        ("17", "Megalaya"),
        ("18", "Assam"),
        ("19", "West Bengal"),
        ("20", "Jharkhand"),
        ("21", "ODISHA"),
        ("22", "CHATTISGARH"),
        ("23", "Madhya Pradesh"),
        ("24", "Gujarat"),
        ("25", "DAMAN AND DIU"),
        ("26", "DADRA AND NAGAR HAVELI"),
        ("27", "Maharashtra"),
        ("38", "ANDHRA PRADESH (BEFORE DIVISION)"),
        ("29", "Karnataka"),
        ("30", "Goa"),
        ("31", "LAKSHADWEEP"),
        ("32", "Kerala"),
        ("33", "Tamil Nadu"),
        ("34", "PUDUCHERRY"),
        ("35", "ANDAMAN AND NICOBAR ISLANDS"),
        ("36", "TELANGANA"),
        ("37", "ANDHRA PRADESH (NEW)"),
    )

REGISTERED_FROM = (
           ('web_app', 'Customer Web App'),
           ('admin_portal', 'Admin Portal'),
        )

COUNTRY_CODE = (
        ('91', 'India'),
    )

ACCOUNT_STATUS = (
           ('A', 'Active'),
           ('I', 'Inactive'),
           ('D', 'Deleted'),
           ('S', 'Suspended'),
        )

PROFILE_STATUS = (
           ('A', 'Active'),
           ('AV', 'Awaiting Account Verification'),
           ('APV', 'Awaiting Phone Number Verification'),
           ('AEV', 'Awaiting Email Verification'),
        )

GENDER = (
           ('M', 'Male'),
           ('F', 'Female'),
           ('O', 'Other'),
        )

COVID_STATUS = (
    ('N', 'Negative'),
    ('P', 'Positive'),
    ('V', 'Verification'),
)

class ContactAddress(models.Model):
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=125, null=True, blank=True)
    street = models.CharField(max_length=125, null=True, blank=True)
    state = models.CharField(choices=STATE_LIST, max_length=125, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=125, null=True, blank=True)
    landmark = models.CharField(max_length=250, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    
    def get_contact_address(self):
        address = ''
        if self.address1:
            address = self.address1
        if self.address2:
            if address:address += ', '
            address = address + self.address2
        if self.city:
            if address:address += ', '
            address = address + self.city
        if self.street:
            if address:address += ', '
            address = address + self.street
        if self.state:
            if address:address += ', '
            address = address + self.state
        if self.country:
            address = address + self.country
        return address
    
    def __unicode__(self):
        if self.address1:
            return str(self.id) + " -- " + self.address1
        return str(self.id)


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile',on_delete = models.CASCADE)
    country_code = models.CharField(choices=COUNTRY_CODE, max_length=50, blank=True, default='91')
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    user_uid = models.CharField(max_length=250, null=True, blank=True)
    registered_from = models.CharField(choices=REGISTERED_FROM, max_length=125, null=True, blank=True, default='web_app')
    refresh_token = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    acc_status = models.CharField(choices=ACCOUNT_STATUS, max_length=125, null=True, blank=True)
    profile_status = models.CharField(choices=PROFILE_STATUS, max_length=125, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=125, null=True, blank=True, default='M')
    address = models.ForeignKey(ContactAddress, null=True, blank=True, on_delete = models.CASCADE)
    profile_pic1 = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    profile_pic2 = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    profile_pic3 = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    sms_alert = models.BooleanField(default=False)
    email_alert = models.BooleanField(default=False)
    member_since = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    remarks = models.TextField(null=True, blank=True)
    address_added = models.BooleanField(default=False)
    fcm_token = models.CharField(max_length=250, null=True, blank=True)
    covid_status = models.CharField(choices=COVID_STATUS, max_length=125, null=True, blank=True, default='N')
    
    def get_full_name(self):
        if self.user.first_name and self.user.last_name:  
            return str(self.user.first_name) + ' ' + str(self.user.last_name)
        elif self.user.first_name:
            return self.user.first_name
        else:
            return "Not Specified"

    def get_user_address(self):
        return self.address.get_contact_address() 
    
    def get_account_status(self):
        return self.get_acc_status_display() 
    
    def get_profile_status(self):
        return self.get_profile_status_display() 
    
    def __unicode__(self):
        return str(self.id) + " -- " + self.user.first_name
    
    class Meta:
        ordering = ('-member_since',)


class UserFeedback(models.Model):
    customer = models.OneToOneField(CustomerProfile, related_name='user_feedback',on_delete = models.CASCADE)
    feedback = models.TextField(max_length=250, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class UserPositivityLog(models.Model):
    customer = models.ForeignKey(CustomerProfile, related_name='postivity_logs',on_delete = models.CASCADE)
    covid_status = models.CharField(choices=COVID_STATUS, max_length=125, null=True, blank=True, default='N')
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']