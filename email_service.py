import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_username = os.getenv("GMAIL_USERNAME")
        self.smtp_password = os.getenv("GMAIL_APP_PASSWORD")

        if not self.smtp_username or not self.smtp_password:
            logger.warning("⚠️ Gmail credentials not found in environment variables")
            logger.warning("⚠️ Email sending will be disabled")
            self.enabled = False
        else:
            self.enabled = True
            logger.info("✅ Email service initialized successfully")

    def _test_connection(self):
        """Тестирование подключения к SMTP серверу"""
        if not self.enabled:
            return False

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.smtp_username, self.smtp_password)
            logger.info("✅ SMTP connection test successful")
            return True
        except Exception as e:
            logger.error(f"❌ SMTP connection test failed: {str(e)}")
            return False

    def format_seats(self, seat_ids):
        """Форматирует список мест в красивый вид: 1,2,3,10,11,12"""
        if not seat_ids:
            return ""

        seat_ids = sorted(seat_ids)
        ranges = []
        start = seat_ids[0]
        end = seat_ids[0]

        for seat in seat_ids[1:]:
            if seat == end + 1:
                end = seat
            else:
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}-{end}")
                start = end = seat

        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{end}")

        return ", ".join(ranges)

    async def send_booking_confirmation(self, to_email: str, movie_title: str, seat_ids: list):
        """Отправка подтверждения бронирования"""
        if not self.enabled:
            logger.info(f"📧 Email sending disabled. Would send to {to_email}: {movie_title} - seats {seat_ids}")
            return {"success": True, "message": "Email simulation"}

        try:
            seats_str = self.format_seats(seat_ids)

            msg = MIMEMultipart('alternative')
            msg['From'] = f"Кинотеатр <{self.smtp_username}>"
            msg['To'] = to_email
            msg['Subject'] = "✅ Подтверждение бронирования в кинотеатре"

            # HTML версия письма
            html_content = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; }}
                    .header {{ background: #ff6b6b; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .details {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                    .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎬 Бронирование подтверждено!</h1>
                    </div>
                    <div class="content">
                        <p>Спасибо за бронирование в нашем кинотеатре!</p>
                        <div class="details">
                            <h3>📋 Детали бронирования:</h3>
                            <p><strong>Фильм:</strong> {movie_title}</p>
                            <p><strong>Места:</strong> {seats_str}</p>
                            <p><strong>Количество мест:</strong> {len(seat_ids)}</p>
                            <p><strong>Email:</strong> {to_email}</p>
                        </div>
                        <p>Ждем вас в кинотеатре!</p>
                    </div>
                    <div class="footer">
                        <p>Это письмо сформировано автоматически. Пожалуйста, не отвечайте на него.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

            # Отправка через SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info(f"✅ Email отправлен на {to_email} для мест {seats_str}")
            return {"success": True, "message": "Email отправлен успешно"}

        except smtplib.SMTPAuthenticationError as e:
            error_msg = "Ошибка аутентификации Gmail. Проверьте логин и пароль приложения"
            logger.error(f"❌ {error_msg}: {str(e)}")
            return {"success": False, "message": error_msg}
        except Exception as e:
            error_msg = f"Ошибка отправки email: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return {"success": False, "message": error_msg}

    async def send_all_bookings(self, to_email: str, bookings_data: list):
        """Отправка всех бронирований пользователя"""
        if not self.enabled:
            logger.info(f"📧 Email sending disabled. Would send all bookings to {to_email}")
            return {"success": True, "message": "Email simulation"}

        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"Кинотеатр <{self.smtp_username}>"
            msg['To'] = to_email
            msg['Subject'] = "🎟️ Все ваши бронирования в кинотеатре"

            # Формируем HTML с всеми бронированиями
            bookings_html = ""
            for booking in bookings_data:
                seats_str = self.format_seats(booking['seat_ids'])
                bookings_html += f"""
                <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px;">
                    <h4>🎬 {booking['movie_title']}</h4>
                    <p><strong>Места:</strong> {seats_str}</p>
                    <p><strong>Дата бронирования:</strong> {booking['booking_date']}</p>
                </div>
                """

            html_content = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; }}
                    .header {{ background: #4ecdc4; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎟️ Все ваши бронирования</h1>
                    </div>
                    <div class="content">
                        <p>Уважаемый клиент, вот все ваши текущие бронирования:</p>
                        {bookings_html}
                        <p>Спасибо, что выбираете наш кинотеатр!</p>
                    </div>
                    <div class="footer">
                        <p>Это письмо сформировано автоматически. Пожалуйста, не отвечайте на него.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

            # Отправка через SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info(f"✅ Все бронирования отправлены на {to_email}")
            return {"success": True, "message": "Все бронирования отправлены на email"}

        except Exception as e:
            error_msg = f"Ошибка отправки всех бронирований: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return {"success": False, "message": error_msg}

# Создаем глобальный экземпляр
email_service = EmailService()