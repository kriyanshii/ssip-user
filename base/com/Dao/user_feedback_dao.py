from base import db
from base.com.Vo.user_feedback_vo import UserFeedbackVo

class UserFeedbackDao:

    def insert_feedback(self,user_feedback_vo):
        db.session.add(user_feedback_vo)
        db.session.commit()

    def view_feedback(self):
        feedback_list = UserFeedbackVo.query.all()
        return feedback_list