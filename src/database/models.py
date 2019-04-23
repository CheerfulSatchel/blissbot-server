from sqlalchemy import Column, Integer, String
from database import Base


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    image_url = Column(String(255))
    title_link = Column(String(255))
    category = Column(String(255))
    meta_content = Column(String(255))

    def __repr__(self):
        return '<Article(id="%s", title="%s", image_url="%s", title_link="%s", category="%s", meta_content="%s"' % (self.id, self.title,
                                                                                                                    self.image_url,
                                                                                                                    self.title_link,
                                                                                                                    self.category,
                                                                                                                    self.meta_content)
