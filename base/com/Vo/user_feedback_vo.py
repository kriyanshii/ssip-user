from base import db

class UserFeedbackVo(db.Model):

    __tablename__ = 'user_feedback_table'
    user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    question_1 = db.Column('question_1', db.Text, nullable=False)
    question_2 = db.Column('question_2', db.Text, nullable=False)
    paragraph = db.Column('paragraph', db.Text, nullable=False)
    police_station_name = db.Column('police_station_name', db.Text, nullable=False)
    district = db.Column('district', db.Text, nullable=False)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'question_1': self.question_1,
            'question_2': self.question_2,
            'paragraph': self.paragraph,
            'police_station_name': self.police_station_name,
            'district': self.district
        }


db.create_all()