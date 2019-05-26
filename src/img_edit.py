import cv2
import numpy
import weather
import datetime

IMG = {"clear sky": "01d.png", "few clouds": "02d.png", "scattered clouds": "03d.png",
           "broken clouds": "04d.png", "overcast clouds": "04.png", "shower rain": "09d.png", "rain": "10d.png",
           "thunderstorm": "11d.png", "snow": "13d.png", "mist": "50d.png"}


def create_forecast_img():
    img_list = [cv2.imread("img/icon/blank.png")]
    forecast = weather.get_days_forecast("Chiba", 1)
    description = forecast[0]
    for img in description:
        img_list.append(cv2.imread("img/icon/"+IMG[img]))
    im_h = cv2.hconcat(img_list)
    cv2.imwrite("img/today_weather.png", im_h)
    print(im_h)


def write_text():
    img_path = "img/today_weather.png"
    img = cv2.imread(img_path)
    today = datetime.date.today()
    text = str((today+datetime.timedelta(days=1)).month)+"/"+str((today+datetime.timedelta(days=1)).day)
    cv2.putText(img, text, (5, 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (0, 0, 0), 1, cv2.LINE_AA)
    for i in range(8):
        if i < 4:
            cv2.putText(img, str(i*3), (53+i*50, 30), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 0, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(img, str(i*3), (43+i*50, 30), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 0, 0), 1, cv2.LINE_AA)
    cv2.imwrite(img_path, img)


if __name__ == '__main__':
    create_forecast_img()
    write_text()
