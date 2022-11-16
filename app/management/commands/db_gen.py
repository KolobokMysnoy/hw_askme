from django.core.management.base import BaseCommand
from app.models import Profile, Question, Answer, Tag, LikeForAnswer, LikeForQuestion
from django.contrib.auth.models import User
import random
import string


class Command(BaseCommand):
    PROFILE_CNT = 10000
    QUESTION_CNT = 100000
    ANSWER_CNT = 1000000
    TAG_CNT = 10000
    LIKE_CNT = 2000000
    USERNAME_MAX_LENGTH = 10
    PASSWORD_MAX_LENGTH = 10
    EMAIL_MAX_LENGTH = 10
    EMAIL_TAIL = '@mail.ru'
    TITLE_MAX_LENGTH = 10
    TEXT_MAX_LENGTH = 30
    RATING_ABS_MAX = 15
    TAG_MAX_LENGTH = 5
    TAG_MAX_FOR_QUESTION = 5
    ANSWER_MAX_FOR_QUESTION = 15
    WORD_MAX_LENGTH = 5

    avatars_set = ('img/baby_boss.jpg', 'img/default_av.png', 'img/diper.jpg', 'img/gryu.png',
                   'img/kick_boot.jpg', 'img/rick&morty.jpg', 'img/vudy.jpg')

    def gen_profiles(self):
        for i in range(self.PROFILE_CNT):
            username = self.gen_word(self.USERNAME_MAX_LENGTH) + '_' + str(i)
            password = self.gen_word(self.PASSWORD_MAX_LENGTH)
            email = self.gen_word(self.EMAIL_MAX_LENGTH) + self.EMAIL_TAIL
            user = User(username=username, password=password,
                        email=email, is_staff=False, is_active=True,
                        is_superuser=False)
            user.save()
            profile = Profile(
                user=user, avatar=random.choice(self.avatars_set))
            profile.save()

    def gen_tags(self):
        tag_list = []
        for i in range(self.TAG_CNT):
            name = self.gen_word(self.TAG_MAX_LENGTH) + '_' + str(i)
            tag = Tag(name=name)
            tag_list.append(tag)
            if (i % 1000 == 0):
                Tag.objects.bulk_create(tag_list)
                tag_list.clear()

        if (len(tag_list) != 0):
            Tag.objects.bulk_create(tag_list)

    def gen_questions(self):
        for _ in range(self.QUESTION_CNT):
            title = self.gen_text(self.TITLE_MAX_LENGTH)
            text = self.gen_text(self.TEXT_MAX_LENGTH)
            owner = random.choice(Profile.objects.all())
            tags = [random.choice(Tag.objects.all()) for _ in
                    range(random.randint(1, self.TAG_MAX_FOR_QUESTION))]
            rating = random.randint(-self.RATING_ABS_MAX, self.RATING_ABS_MAX)
            answer_cnt = random.randint(0, self.RATING_ABS_MAX)

            question = Question(title=title, text=text, owner=owner,
                                rating=rating, answer_cnt=answer_cnt)
            question.save()
            question.tags.set(tags)

    def gen_answers(self):
        answer_list = []
        for i in range(self.ANSWER_CNT):
            text = self.gen_text(self.TEXT_MAX_LENGTH)
            owner = random.choice(Profile.objects.all())
            question = random.choice(Question.objects.all())
            rating = random.randint(-self.RATING_ABS_MAX, self.RATING_ABS_MAX)
            answer = Answer(text=text, owner=owner,
                            question=question, rating=rating)
            answer_list.append(answer)
            if (i % 1000 == 0):
                Answer.objects.bulk_create(answer_list)
                answer_list.clear()
        if (len(answer_list) != 0):
            Answer.objects.bulk_create(answer_list)

    def gen_likes_for_questions(self):
        like_question_list = []
        owners = Profile.objects.all()
        questions = Question.objects.all()
        count = self.LIKE_CNT
        for owner in owners:
            for question in questions:
                is_like = random.choice([True, False])
                like = LikeForQuestion(
                    owner=owner, question=question, is_like=is_like)
                like_question_list.append(like)
                if (len(like_question_list) == 1000):
                    LikeForQuestion.objects.bulk_create(like_question_list)
                    like_question_list.clear()
                    count -= 1000
                    if (count <= 0):
                        return

        if (len(like_question_list) != 0):
            LikeForQuestion.objects.bulk_create(like_question_list)
            like_question_list.clear()

    def gen_likes_for_answers(self):
        like_answer_list = []
        answers = Answer.objects.all()
        owners = Profile.objects.all()
        count = self.LIKE_CNT
        for owner in owners:
            for answer in answers:
                is_like = random.choice([True, False])
                like = LikeForAnswer(
                    owner=owner, answer=answer, is_like=is_like)
                like_answer_list.append(like)
                if (len(like_answer_list) == 1000):
                    LikeForAnswer.objects.bulk_create(like_answer_list)
                    like_answer_list.clear()
                    count -= 1000
                    if (count <= 0):
                        return

        if (len(like_answer_list) != 0):
            LikeForAnswer.objects.bulk_create(like_answer_list)
            like_answer_list.clear()

    def gen_text(self, max: int):
        symbol_cnt = random.randrange(max // 2, max, 1)
        text = ''
        while len(text) < symbol_cnt:
            word = self.gen_word(self.WORD_MAX_LENGTH)
            text += word + ' '
        return text

    def gen_word(self, max: int):
        return ''.join(random.choice(string.ascii_letters + string.digits)
                       for _ in range(random.randint(1, max)))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start generatrion!"))
        self.gen_profiles()
        self.stdout.write(self.style.SUCCESS("Users and profiles created!"))
        self.gen_tags()
        self.stdout.write(self.style.SUCCESS("Tags created!"))
        self.gen_questions()
        self.stdout.write(self.style.SUCCESS("Questions created!"))
        self.gen_answers()
        self.stdout.write(self.style.SUCCESS("Answers created!"))
        self.gen_likes_for_questions()
        self.stdout.write(self.style.SUCCESS("Likes for questions created!"))
        self.gen_likes_for_answers()
        self.stdout.write(self.style.SUCCESS("Likes for answers created!"))
