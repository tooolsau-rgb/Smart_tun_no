import json, threading
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import requests

Window.clearcolor=(.055,.075,.12,1)
BG=(.08,.12,.19,1); ACCENT=(.16,.57,.91,1)

class SmartClaw(App):
    def build(self):
        self.title='SmartClaw'
        root=BoxLayout(orientation='vertical',padding=dp(16),spacing=dp(10))
        root.add_widget(Label(text='SMARTCLAW  •  VPS CONTROL',font_size='22sp',bold=True,size_hint_y=None,height=dp(48),color=(.65,.85,1,1)))
        self.url=TextInput(hint_text='HTTPS bridge URL (e.g. https://host.tailnet.ts.net)',multiline=False,size_hint_y=None,height=dp(48),background_color=BG,foreground_color=(1,1,1,1),hint_text_color=(.6,.7,.8,1))
        self.token=TextInput(hint_text='Bridge token (NOT Telegram/Gateway token)',password=True,multiline=False,size_hint_y=None,height=dp(48),background_color=BG,foreground_color=(1,1,1,1))
        root.add_widget(self.url);root.add_widget(self.token)
        nav=BoxLayout(size_hint_y=None,height=dp(45),spacing=dp(8))
        for title,path in [('Kiểm tra','/health'),('Trạng thái','/status'),('Nodes','/nodes')]:
            b=Button(text=title,background_normal='',background_color=ACCENT)
            b.bind(on_release=lambda _,p=path:self.fetch('GET',p))
            nav.add_widget(b)
        root.add_widget(nav)
        scroll=ScrollView()
        self.log=Label(text='Chào mừng! Nhập URL HTTPS và Bridge Token để kết nối.\nKhông nhúng bí mật vào APK.',markup=False,size_hint_y=None,halign='left',valign='top',color=(.92,.95,1,1),font_size='15sp')
        self.log.bind(texture_size=lambda instance,size:setattr(instance,'height',max(dp(300),size[1]+dp(20))))
        self.log.bind(width=lambda instance,value:setattr(instance,'text_size',(value-dp(12),None)))
        scroll.add_widget(self.log);root.add_widget(scroll)
        self.message=TextInput(hint_text='Nhập câu hỏi cho OpenClaw...',multiline=True,size_hint_y=None,height=dp(86),background_color=BG,foreground_color=(1,1,1,1))
        root.add_widget(self.message)
        send=Button(text='GỬI TIN NHẮN',size_hint_y=None,height=dp(52),background_normal='',background_color=ACCENT,bold=True)
        send.bind(on_release=self.send);root.add_widget(send)
        root.add_widget(Label(text='Chỉ dùng với VPS của bạn • TLS + Tailscale',font_size='11sp',color=(.6,.7,.8,1),size_hint_y=None,height=dp(24)))
        return root
    def append(self,text):
        Clock.schedule_once(lambda _:setattr(self.log,'text',self.log.text+'\n\n'+str(text)),0)
    def send(self,*_):
        msg=self.message.text.strip()
        if not msg:return
        self.append('Bạn: '+msg);self.message.text='';self.fetch('POST','/chat',{'message':msg})
    def fetch(self,method,path,payload=None):
        url=self.url.text.strip().rstrip('/')
        if not url.startswith('https://'):
            self.append('Lỗi: URL phải dùng HTTPS.');return
        token=self.token.text.strip()
        if not token:self.append('Thiếu Bridge Token.');return
        def job():
            try:
                r=requests.request(method,url+path,json=payload,headers={'Authorization':'Bearer '+token},timeout=135 if path=='/chat' else 45)
                data=r.json()
                if r.status_code>=400:self.append(f'Lỗi HTTP {r.status_code}: {data.get("error",data.get("output","Unknown"))}')
                elif path=='/chat':self.append('OpenClaw: '+data.get('output','(Không có nội dung)'))
                else:self.append(path+':\n'+json.dumps(data,ensure_ascii=False,indent=2))
            except Exception as e:self.append('Lỗi kết nối: '+str(e))
        threading.Thread(target=job,daemon=True).start()

if __name__=='__main__':SmartClaw().run()
