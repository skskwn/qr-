
#이미지는 저작권으로 삭제하였습니다. 이미지 필요시 코드에 '#'을 지우고 경로에 맞게 이미지 파일 이름을 변경 후 사용

import os, sys
from tkinter import Image

import qrcode



from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *




import firebase_admin
from datashape import unicode
from firebase_admin import credentials
from firebase_admin import db


#Firebase database 인증
from qtconsole.qt import QtCore, QtGui

cred = credentials.Certificate(' Firebase인증 json파일 이름 ')
firebase_admin.initialize_app(cred,{
    'databaseURL' : ' Firebase url 주소 '
})







#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야합니다.



uifile_1 = 'untitled.ui'
form_1, base_1 = uic.loadUiType(uifile_1)

uifile_2 = 'untitled1.ui'
form_2, base_2 = uic.loadUiType(uifile_2)

uifile_3 = 'untitled2.ui'
form_3, base_3 = uic.loadUiType(uifile_3)



#화면을 띄우는데 사용되는 Class 선언
class login(base_1, form_1):


    def __init__(self) :
        super(base_1,self).__init__()
        self.setupUi(self)

        #아이콘 설정
        #self.setWindowIcon(QIcon('./icon.png')) #이미지를 사용하고 싶다면  '#'를 지우고 사용

        # 버튼 숨기기
        self.pushButton_qr.hide()

        # 창 조절 금지
        self.setFixedSize(331, 555)

        # QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        #self.qPixmapFileVar = QPixmap() #이미지를 사용하고 싶다면  '#'를 지우고 사용
        #self.qPixmapFileVar.load("./image.png") #이미지를 사용하고 싶다면  '#'를 지우고 사용
        #self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(120) #이미지를 사용하고 싶다면  '#'를 지우고 사용
        #self.label_logo.resize(200, 200) #이미지를 사용하고 싶다면  '#'를 지우고 사용
        #self.label_logo.setPixmap(self.qPixmapFileVar) #이미지를 사용하고 싶다면  '#'를 지우고 사용

        # 백그라운드 색을 흰색으로 표시
        self.label_background.setStyleSheet("background-color: #ffffff")

        # QR를 파랑으로 표시
        self.label_QR.setStyleSheet("color: #5f9ccb")

        # code login를 하늘로 표시
        self.label_CodeLogin.setStyleSheet("color: #49799e")


        # qr입력 버튼 이미지 씌우기
        #self.pushButton_qr.setStyleSheet('image:url(./image1.png);border:0px;') #이미지를 사용하고 싶다면  '#'를 지우고 사용

        # 이름칸 & key칸에 글씨가 바뀌었을 때 버튼표시
        self.lineEdit_name.textChanged.connect(self.lineeditTextFunction)

        # qr 버튼 클릭했을 때
        self.pushButton_qr.clicked.connect(self.pushButton_qr_clicked)  # 클릭 시 실행할 function


    # 이름칸 & key칸에 글씨가 바뀌었을 때 버튼표시
    def lineeditTextFunction(self):
        self.pushButton_qr.show()

    # qr 버튼 클릭했을 때
    def pushButton_qr_clicked(self):

        self.label_notice.setText("잠시만 기다려주세요...")

        # 전역변수 설정
        global name

        # 전역변수 name에 이름값 전달
        name = self.lineEdit_name.text()
        ref0 = db.reference('Key/key')
        key1 = self.lineEdit_key.text()

        if (ref0.get() == key1):
            # qr인증 페이지 설정 & 나타내기
            self.label_notice.setText("인증대기...")
            self.close()
            self.main = qr()
            self.main.show()

        else:
            # 로그인 실패시 Label 설정
            self.label_notice.setText("등록되지 않는 이름이거나 인증 key가 틀렸습니다.")






# QR 코드용 이미지 클래스
class Image(qrcode.image.base.BaseImage):


    # qr생성
    def __init__(self, border, width, box_size):
        # 경계 지정
        self.border = border


        # 너비 할당
        self.width = width

        # 할당된 박스 사이즈
        self.box_size = box_size

        # 크기 생성
        size = (width + border * 2) * box_size

        # 이미지
        self._image = QImage(size, size, QImage.Format_RGB16)

        # 초기 이미지를 흰색으로
        self._image.fill(Qt.white)

        # 픽스맵 방법

    def pixmap(self):
        # 이미지를 반환
        return QPixmap.fromImage(self._image)

        # 사각형 그리기를위한 drawrect 메서드

    def drawrect(self, row, col):
        # creating painter object
        painter = QPainter(self._image)

        # 직사각형 그리기
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            QtCore.Qt.black)




# qr 인증 페이지
class qr(base_2, form_2):
    def __init__(self):
        super(base_2, self).__init__()
        self.setupUi(self)

        # 아이콘 설정
        self.setWindowIcon(QIcon('./icon.png'))

        # 창 조절 금지
        self.setFixedSize(341, 495)

        ref = db.reference('qr인증/' + name + '/qrcode')

        # qr 코드의 pix 맵 생성
        qr_image = qrcode.make(ref.get(), image_factory=Image).pixmap()

        # 라벨에 이미지 설정
        self.label_qr.setPixmap(qr_image)

        # QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        #self.qPixmapFileVar = QPixmap() #이미지를 사용하고 싶다면  '#'를 지우고 사용
        #self.qPixmapFileVar.load("./logo1.png") #이미지를 사용하고 싶다면  '#'를 지우고 사용
        #self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(50) #이미지를 사용하고 싶다면  '#'를 지우고 사용
        #self.label_logo.resize(51, 51) #이미지를 사용하고 싶다면  '#'를 지우고 사용
        #self.label_logo.setPixmap(self.qPixmapFileVar) #이미지를 사용하고 싶다면  '#'를 지우고 사용

        # qrcode 버튼 클릭했을 때
        self.pushButton_qrcode1.clicked.connect(self.pushButton_qrcode_clicked)  # 클릭 시 실행할 function

        # qr입력 버튼 이미지 씌우기
        #self.pushButton_qrcode1.setStyleSheet('image:url(./image2.png);border:0px;') #이미지를 사용하고 싶다면  '#'를 지우고 사용

        # 전역변수 설정
        global passage

        #오프라인 설정
        passage = 0

    # qrcode 버튼 클릭했을 때
    def pushButton_qrcode_clicked(self):

        # 전역변수 name값을 가져와 qr인증 되었는지 확인
        ref1 = db.reference('qr인증/' + name + '/qr인증')

        # 가져온 값에 따라 로그인 허용
        if (ref1.get() == 1):
            self.label_text.setText("인증완료")
            # 오프라인 금지
            global passage
            passage = 1
            self.close()
            self.Home = Home()
            self.Home.show()



        else:
            self.label_text.setText("QR Code 인증을 완료해주세요.")


    # 인증완료 버튼이 눌리지 않으면 로그아웃처리 눌렸으면 로그인처리
    def closeEvent(self, event):
        if (passage == 0):
            ref7 = db.reference('qr인증/' + name)
            ref7.update({'qr인증': 0})



# Home 페이지
class Home(base_3, form_3):
    def __init__(self):
        super(base_3, self).__init__()
        self.setupUi(self)

        # 창 조절 금지
        self.setFixedSize(370, 613)








if __name__ == '__main__':

       app = QApplication(sys.argv)
       ex = login()
       ex.show()
       sys.exit(app.exec_())
