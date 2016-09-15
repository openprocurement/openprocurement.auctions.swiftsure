��                             �       �       K       g  
   v     �  !   �  h   �       �   !  �        �  
   	  ~     P   �     �  D   �     2	     A	  I   X	  v   �	  !   
  t   ;
  Z   �
  �     9   �  G   �  W   =    �     �  O  �  t  �     b  @       �     �     �  =     �   L       �  +  |  �     )     E  #  a  �   �  
   "  \   -     �  '   �  Z   �  �   %  >     �   D  �   �  �   v  O   a  G   �  �   �   0.1 API accepts `JSON <http://json.org/>`_ or form-encoded content in requests.  It returns JSON content in all of its responses, including errors.  Only the UTF-8 character encoding is supported for both requests and responses. API is highly unstable, and while API endpoints are expected to remain relatively stable the data exchange formats are expected to be changed a lot.  The changes in the API are communicated via `Open Procurement API <https://groups.google.com/group/open-procurement-api>`_ maillist. API stability All API POST and PUT requests expect a top-level object with a single element in it named `data`.  Successful responses will mirror this format. The data element should itself be an object, containing the parameters for the request.  In the case of creating a new auction, these are the fields we want to set on the auction itself. Business logic Change log Conventions Documentation of related packages During *active.tendering* period participants can ask questions, submit proposals, and upload documents. Features If something went wrong during the request, we'll get a different status code and the JSON returned will have an `errors` field at the top level containing a list of problems.  We look at the first one and print out its message. If the request was successful, we will get a response code of `201` indicating the object was created.  That response will have a data field at its top level, which will contain complete information on the new auction, including its ID. Main responsibilities Next steps No need to specify enquiries period (there is no *active.enquiries* status), since it overlaps with *active.tendering* period. Organizer can't edit procedure's significant properties (*Auction.value*, etc.). Overview Procedure can be switched from *draft* status to *active.tendering*. Project status Released: not released The only currency (*Value.currency*) for this procedure is hryvnia (UAH). The only date Organizer has to provide is *Tender.auctionPeriod.startDate*, the rest will be calculated automatically. The project has pre alpha status. The source repository for this project is on GitHub: https://github.com/openprocurement/openprocurement.auctions.dgf There is obligatory participant qualification (*Bid.selfQualified*) via guarantee payment. You can leave feedback by raising a new issue on the `issue tracker <https://github.com/openprocurement/openprocurement.auctions.dgf/issues>`_ (GitHub registration necessary). You might find it helpful to look at the :ref:`tutorial`. `OpenProcurement API <http://api-docs.openprocurement.org/en/latest/>`_ openprocurement.auctions.dgf contains documentaion for Deposit Guarantee Fund auctions. Project-Id-Version: openprocurement.auctions.dgf 0.1
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2016-09-12 15:36+0300
PO-Revision-Date: 2016-09-15 13:19+0200
Last-Translator: Zoriana Zaiats <sorenabell@quintagroup.com>
Language-Team: Ukrainian <support@quintagroup.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Language: uk
Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);
X-Generator: Lokalize 2.0
 0.1 API приймає `JSON <http://json.org/>`_ або form-encoded вміст у запитах. Він повертає JSON вміст у всіх свої відповідях, включно з помилками. Підтримується лише UTF-8 кодування і для запитів, і для відповідей. API є дуже нестабільним. Хоча точки входу API будуть відносно стабільними, формати обміну даними будуть часно змінюватись. Зміни в API обговорюються через `Open Procurement API <https://groups.google.com/group/open-procurement-api>`_ розсилку. Стабільність API Всі API POST та PUT запити очікують об'єкт верхнього рівня з єдиним елементом з назвою `data`. Відповіді з повідомленням про успіх будуть віддзеркалювати цей формат. Елемент data повинен сам бути об’єктом, що містить параметри запиту. Якщо створюється новий аукціон, то це ті поля, які ми хочемо встановити на самому аукціоні. Бізнес логіка Звіт про зміни Домовленості Документація пов’язаних пакетів Протягом періоду *active.tendering* учасники можуть задавати питання, подавати пропозиції, завантажувати документи. Особливості Якщо під час запиту виникли труднощі, ми отримаємо інший код стану та JSON, який при поверненні міститиме `errors` поле на верхньому рівні зі списком проблем. Ми дивимось на першу з них і видруковуємо її повідомлення. Якщо запит був успішним, ми отримаємо код відповіді `201`, який вказує, що об’єкт був створений. Ця відповідь буде мати data поле на верхньому рівні, яке вміщуватиме повну інформацію про новий аукціон, включно з ID. Основні задачі Наступні кроки Відсутність необхідності вказання періоду уточнень (тут немає окремого статусу *active.enquiries*), оскільки він накладається на період прийому пропозицій *active.tendering*. Організатор не може редагувати суттєвих властивостей процедури, наприклад, *Auction.value*. Огляд Процедура переходить зі статусу *draft* до *active.tendering*. Стан проекту Випущено: не випущено Єдина валюта (*Value.currency*) цієї процедури - гривня UAH. Єдина дата, яку потрібно надати, це дата початку аукціону *Tender.auctionPeriod.startDate*. Всі решта дати будуть обраховані на її основі. Статус цього проекту - перед-альфа Репозиторій джерельних текстів цього проекту є на `GitHub <https://github.com/openprocurement/openprocurement.auctions.dgf>`_. Обов’язкова кваліфікація учасника (*Bid.selfQualified*) через гарантійний платіж. Повідомляйте про всі проблеми та поради через `issue tracker <https://github.com/openprocurement/openprocurement.auctions.dgf/issues>`_ (реєстрація на GitHub обов’язкова). Можливо вам буде цікаво прочитати :ref:`tutorial`. `OpenProcurement API <http://api-docs.openprocurement.org/en/latest/>`_ openprocurement.auctions.dgf містить документацію по аукціонах Фонду гарантування вкладів. 