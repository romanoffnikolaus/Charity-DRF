from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from slugify import slugify
from program_categories.models import Category



class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractUser):
    objects = UserManager()
    
    slug = models.SlugField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    user_photo = models.ImageField(upload_to='account/', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    twitter_url = models.URLField(max_length=255, blank=True)
    facebook_url = models.URLField(max_length=255, blank=True)
    telegram_url = models.URLField(max_length=255, blank=True)
    about_user = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    adress = models.CharField(max_length=150, blank=True)
    requisites = models.CharField(max_length=150, blank=True)
    
    region_fields = (('Afghanistan', 'Afghanistan'), ('land Islands', 'land Islands'), ('Albania', 'Albania'), ('Algeria', 'Algeria'), ('American Samoa', 'American Samoa'), ('AndorrA', 'AndorrA'), ('Angola', 'Angola'), ('Anguilla', 'Anguilla'), ('Antarctica', 'Antarctica'), ('Antigua and Barbuda', 'Antigua and Barbuda'), ('Argentina', 'Argentina'), ('Armenia', 'Armenia'), ('Aruba', 'Aruba'), ('Australia', 'Australia'), ('Austria', 'Austria'), ('Azerbaijan', 'Azerbaijan'), ('Bahamas', 'Bahamas'), ('Bahrain', 'Bahrain'), ('Bangladesh', 'Bangladesh'), ('Barbados', 'Barbados'), ('Belarus', 'Belarus'), ('Belgium', 'Belgium'), ('Belize', 'Belize'), ('Benin', 'Benin'), ('Bermuda', 'Bermuda'), ('Bhutan', 'Bhutan'), ('Bolivia', 'Bolivia'), ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'), ('Botswana', 'Botswana'), ('Bouvet Island', 'Bouvet Island'), ('Brazil', 'Brazil'), ('British Indian Ocean Territory', 'British Indian Ocean Territory'), ('Brunei Darussalam', 'Brunei Darussalam'), ('Bulgaria', 'Bulgaria'), ('Burkina Faso', 'Burkina Faso'), ('Burundi', 'Burundi'), ('Cambodia', 'Cambodia'), ('Cameroon', 'Cameroon'), ('Canada', 'Canada'), ('Cape Verde', 'Cape Verde'), ('Cayman Islands', 'Cayman Islands'), ('Central African Republic', 'Central African Republic'), ('Chad', 'Chad'), ('Chile', 'Chile'), ('China', 'China'), ('Christmas Island', 'Christmas Island'), ('Cocos (Keeling), Islands', 'Cocos (Keeling), Islands'), ('Colombia', 'Colombia'), ('Comoros', 'Comoros'), ('Congo', 'Congo'), ('CongoThe Democratic Republic of the', 'CongoThe Democratic Republic of the'), ('Cook Islands', 'Cook Islands'), ('Costa Rica', 'Costa Rica'), ("Cote D'Ivoire", "Cote D'Ivoire"), ('Croatia', 'Croatia'), ('Cuba', 'Cuba'), ('Cyprus', 'Cyprus'), ('Czech Republic', 'Czech Republic'), ('Denmark', 'Denmark'), ('Djibouti', 'Djibouti'), ('Dominica', 'Dominica'), ('Dominican Republic', 'Dominican Republic'), ('Ecuador', 'Ecuador'), ('Egypt', 'Egypt'), ('El Salvador', 'El Salvador'), ('Equatorial Guinea', 'Equatorial Guinea'), ('Eritrea', 'Eritrea'), ('Estonia', 'Estonia'), ('Ethiopia', 'Ethiopia'), ('Falkland Islands (Malvinas),', 'Falkland Islands (Malvinas),'), ('Faroe Islands', 'Faroe Islands'), ('Fiji', 'Fiji'), ('Finland', 'Finland'), ('France', 'France'), ('French Guiana', 'French Guiana'), ('French Polynesia', 'French Polynesia'), ('French Southern Territories', 'French Southern Territories'), ('Gabon', 'Gabon'), ('Gambia', 'Gambia'), ('Georgia', 'Georgia'), ('Germany', 'Germany'), ('Ghana', 'Ghana'), ('Gibraltar', 'Gibraltar'), ('Greece', 'Greece'), ('Greenland', 'Greenland'), ('Grenada', 'Grenada'), ('Guadeloupe', 'Guadeloupe'), ('Guam', 'Guam'), ('Guatemala', 'Guatemala'), ('Guernsey', 'Guernsey'), ('Guinea', 'Guinea'), ('Guinea-Bissau', 'Guinea-Bissau'), ('Guyana', 'Guyana'), ('Haiti', 'Haiti'), ('Heard Island and Mcdonald Islands', 'Heard Island and Mcdonald Islands'), ('Holy See (Vatican City State),', 'Holy See (Vatican City State),'), ('Honduras', 'Honduras'), ('Hong Kong', 'Hong Kong'), ('Hungary', 'Hungary'), ('Iceland', 'Iceland'), ('India', 'India'), ('Indonesia', 'Indonesia'), ('IranIslamic Republic Of', 'IranIslamic Republic Of'), ('Iraq', 'Iraq'), ('Ireland', 'Ireland'), ('Isle of Man', 'Isle of Man'), ('Israel', 'Israel'), ('Italy', 'Italy'), ('Jamaica', 'Jamaica'), ('Japan', 'Japan'), ('Jersey', 'Jersey'), ('Jordan', 'Jordan'), ('Kazakhstan', 'Kazakhstan'), ('Kenya', 'Kenya'), ('Kiribati', 'Kiribati'), ("KoreaDemocratic People'S Republic of", "KoreaDemocratic People'S Republic of"), ('KoreaRepublic of', 'KoreaRepublic of'), ('Kuwait', 'Kuwait'), ('Kyrgyzstan', 'Kyrgyzstan'), ("Lao People'S Democratic Republic", "Lao People'S Democratic Republic"), ('Latvia', 'Latvia'), ('Lebanon', 'Lebanon'), ('Lesotho', 'Lesotho'), ('Liberia', 'Liberia'), ('Libyan Arab Jamahiriya', 'Libyan Arab Jamahiriya'), ('Liechtenstein', 'Liechtenstein'), ('Lithuania', 'Lithuania'), ('Luxembourg', 'Luxembourg'), ('Macao', 'Macao'), ('MacedoniaThe Former Yugoslav Republic of', 'MacedoniaThe Former Yugoslav Republic of'), ('Madagascar', 'Madagascar'), ('Malawi', 'Malawi'), ('Malaysia', 'Malaysia'), ('Maldives', 'Maldives'), ('Mali', 'Mali'), ('Malta', 'Malta'), ('Marshall Islands', 'Marshall Islands'), ('Martinique', 'Martinique'), ('Mauritania', 'Mauritania'), ('Mauritius', 'Mauritius'), ('Mayotte', 'Mayotte'), ('Mexico', 'Mexico'), ('MicronesiaFederated States of', 'MicronesiaFederated States of'), ('MoldovaRepublic of', 'MoldovaRepublic of'), ('Monaco', 'Monaco'), ('Mongolia', 'Mongolia'), ('Montenegro', 'Montenegro'), ('Montserrat', 'Montserrat'), ('Morocco', 'Morocco'), ('Mozambique', 'Mozambique'), ('Myanmar', 'Myanmar'), ('Namibia', 'Namibia'), ('Nauru', 'Nauru'), ('Nepal', 'Nepal'), ('Netherlands', 'Netherlands'), ('Netherlands Antilles', 'Netherlands Antilles'), ('New Caledonia', 'New Caledonia'), ('New Zealand', 'New Zealand'), ('Nicaragua', 'Nicaragua'), ('Niger', 'Niger'), ('Nigeria', 'Nigeria'), ('Niue', 'Niue'), ('Norfolk Island', 'Norfolk Island'), ('Northern Mariana Islands', 'Northern Mariana Islands'), ('Norway', 'Norway'), ('Oman', 'Oman'), ('Pakistan', 'Pakistan'), ('Palau', 'Palau'), ('Palestinian TerritoryOccupied', 'Palestinian TerritoryOccupied'), ('Panama', 'Panama'), ('Papua New Guinea', 'Papua New Guinea'), ('Paraguay', 'Paraguay'), ('Peru', 'Peru'), ('Philippines', 'Philippines'), ('Pitcairn', 'Pitcairn'), ('Poland', 'Poland'), ('Portugal', 'Portugal'), ('Puerto Rico', 'Puerto Rico'), ('Qatar', 'Qatar'), ('Reunion', 'Reunion'), ('Romania', 'Romania'), ('Russian Federation', 'Russian Federation'), ('RWANDA', 'RWANDA'), ('Saint Helena', 'Saint Helena'), ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'), ('Saint Lucia', 'Saint Lucia'), ('Saint Pierre and Miquelon', 'Saint Pierre and Miquelon'), ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'), ('Samoa', 'Samoa'), ('San Marino', 'San Marino'), ('Sao Tome and Principe', 'Sao Tome and Principe'), ('Saudi Arabia', 'Saudi Arabia'), ('Senegal', 'Senegal'), ('Serbia', 'Serbia'), ('Seychelles', 'Seychelles'), ('Sierra Leone', 'Sierra Leone'), ('Singapore', 'Singapore'), ('Slovakia', 'Slovakia'), ('Slovenia', 'Slovenia'), ('Solomon Islands', 'Solomon Islands'), ('Somalia', 'Somalia'), ('South Africa', 'South Africa'), ('South Georgia and the South Sandwich Islands', 'South Georgia and the South Sandwich Islands'), ('Spain', 'Spain'), ('Sri Lanka', 'Sri Lanka'), ('Sudan', 'Sudan'), ('Suriname', 'Suriname'), ('Svalbard and Jan Mayen', 'Svalbard and Jan Mayen'), ('Swaziland', 'Swaziland'), ('Sweden', 'Sweden'), ('Switzerland', 'Switzerland'), ('Syrian Arab Republic', 'Syrian Arab Republic'), ('TaiwanProvince of China', 'TaiwanProvince of China'), ('Tajikistan', 'Tajikistan'), ('TanzaniaUnited Republic of', 'TanzaniaUnited Republic of'), ('Thailand', 'Thailand'), ('Timor-Leste', 'Timor-Leste'), ('Togo', 'Togo'), ('Tokelau', 'Tokelau'), ('Tonga', 'Tonga'), ('Trinidad and Tobago', 'Trinidad and Tobago'), ('Tunisia', 'Tunisia'), ('Turkey', 'Turkey'), ('Turkmenistan', 'Turkmenistan'), ('Turks and Caicos Islands', 'Turks and Caicos Islands'), ('Tuvalu', 'Tuvalu'), ('Uganda', 'Uganda'), ('Ukraine', 'Ukraine'), ('United Arab Emirates', 'United Arab Emirates'), ('United Kingdom', 'United Kingdom'), ('United States', 'United States'), ('United States Minor Outlying Islands', 'United States Minor Outlying Islands'), ('Uruguay', 'Uruguay'), ('Uzbekistan', 'Uzbekistan'), ('Vanuatu', 'Vanuatu'), ('Venezuela', 'Venezuela'), ('Viet Nam', 'Viet Nam'), ('Virgin IslandsBritish', 'Virgin IslandsBritish'), ('Virgin IslandsU.S.', 'Virgin IslandsU.S.'), ('Wallis and Futuna', 'Wallis and Futuna'), ('Western Sahara', 'Western Sahara'), ('Yemen', 'Yemen'), ('Zambia', 'Zambia'), ('Zimbabwe', 'Zimbabwe'))

    region = models.CharField(max_length=50, choices=region_fields, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    choices=(
                ('default_user', 'Default user (Donations only)'),
                ('user_helper', 'User helper (Creating charity programs)'),
                ('fund', 'Fund (Creating charity programs as organization)')
            )
    user_type = models.CharField(max_length=30, blank=True, choices=choices, help_text='Select user type')

    verified_account = models.BooleanField(default=False)
    
    activation_code = models.CharField(max_length=10, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def create_activation_code(self):
        code = get_random_string(10)
        self.activation_code = code
        self.save()