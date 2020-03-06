from django import forms
from coreSys.models import Member


class MemberForm(forms.ModelForm):
    # Member 테이블의 'expiration' 필드는 읽기 전용으로 결과만 보여준다.
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['expiration'].widget.attrs['readonly'] = True

    class Meta:
        model = Member
        fields = ['name', 'phone', 'member_car_number', 'expiration']
        labels = {
            'name': "이름",
            'phone': "전화번호",
            'member_car_number': "자동차 번호",
            'expiration': "회원 만료일",
        }
        help_texts = {
            'phone': None,
        }
