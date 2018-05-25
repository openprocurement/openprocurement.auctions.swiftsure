.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Auction, Auction
.. _auction:

Auction
=======

Schema
------

:title:
  string, multilingual, required

  The name of the auction, displayed in listings. 
  Originates from `lot.title`.

:description:
  string, multilingual, required

  Detailed auction description. 
  Originates from `lot.description`.

:auctionID:
  string, auto-generated, read-only

  The auction identifier to refer to in "paper" documentation. 

  |ocdsDescription|
  AuctionID should always be the same as the OCID. It is included to make the flattened data structure more convenient.
    
:procurementMethodType:
  string, required
    
  Type of the procedure within the auction announcement. 
  Originates from `lot.auctions.procurementMethodType`.
     
:procuringEntity:
  :ref:`ProcuringEntity`, required

  Organization conducting the auction.
  Originates from `lot.lotCustodian`.
   
  |ocdsDescription|
  The entity managing the procurement, which may be different from the buyer who is paying / using the items being procured.

:tenderAttempts:
  integer, required

  The number which represents what time auction is taking place.
  Originates from `lot.auctions.tenderAttempts`

:value:
  :ref:`value`, required

  Auction starting price. Originates from `lots.auctions.value`. 
  Bids lower than ``value`` will be rejected.

  |ocdsDescription|
  The total estimated value of the procurement.

:guarantee:
  :ref:`Guarantee`, required

  Bid guarantee. Originates from `lot.auctions.guarantee`.

:registrationFee:
  :ref:`Guarantee`, required

  Bid registration fee. Originates from `lot.auctions.registrationFee`.

:bankAccount:
  `bankAccount <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/standard/auction.html#bank-account>`_, optional

  Details which uniquely identify a bank account, and are used when making or receiving a payment.
  Originates from `lot.auctions.bankAccount`.

:items:
  list of :ref:`item` objects, required

  List that contains single item being sold. Originates from `lots.items`.

  |ocdsDescription|
  The goods and services to be purchased, broken into line items wherever possible. Items should not be duplicated, but a quantity of 2 specified instead.

:documents:
  List of :ref:`document` objects
 
  |ocdsDescription|
  All documents and attachments related to the auction.

:questions:
  List of :ref:`question` objects, optional

  Questions to `procuringEntity` and answers to them.

:complaints:
  List of :ref:`complaint` objects, optional

  Complaints to auction conditions and their resolutions.

:bids:
  List of :ref:`bid` objects

  A list of all bids placed in the auction with information about participants, their proposals and other qualification documentation.

  |ocdsDescription|
  A list of all the companies who entered submissions for the auction.

:minimalStep:
  :ref:`value`, required

  Auction step (increment). Originates from `lot.auctions.minimalStep`.

:awards:
  List of :ref:`award` objects

  All qualifications (disqualifications and awards).

:contracts:
  List of :ref:`Contract` objects

:enquiryPeriod:
  :ref:`period`, auto-generated

  Period when questions are allowed.

  |ocdsDescription|
  The period during which enquiries may be made and will be answered.

:tenderPeriod:
  :ref:`period`, auto-generated

  Period when bids can be submitted.

  |ocdsDescription|
  The period when the auction is open for submissions. The end date is the closing date for auction submissions.

:auctionPeriod:
  :ref:`period`, auto-generated

  Period when Auction is conducted. `startDate` originates from `lot.auctions.auctionPeriod.startDate .

:auctionUrl:
  url, auto-generated

  A web address where auction is accessible for view.

:awardPeriod:
  :ref:`period`, auto-generated

  Awarding process period.

  |ocdsDescription|
  The date or period on which an award is anticipated to be made.

:status:
  string, reuired

  :`pending.activation`:
      Procedure activation
  :`active.tendering`:
      Tendering period (tendering)
  :`active.auction`:
      Auction period (auction)
  :`active.qualification`:
      Winner qualification (qualification)
  :`active.awarded`:
      Contract signing
  :`unsuccessful`:
      Unsuccessful auction (unsuccessful)
  :`complete`:
      Complete auction (complete)
  :`cancelled`:
      Cancelled auction (cancelled)

  Status of the procedure.

:cancellations:
  List of :ref:`cancellation` objects.

  Contains 1 object with `active` status in case of cancelled Auction.

  The :ref:`cancellation` object describes the reason of auction cancellation and contains accompanying
  documents  if there are any.

:revisions:
  List of :ref:`revision` objects, auto-generated

  Historical changes to `Auction` object properties.
  
:merchandisingObject:
  string, auto-generated, read-only
  
  Lot's id.
  
.. _Auction Parameters:
  
Auction Parameters
====

Schema
------

:type:	
    string, auto-generated, read-only

    Type of the auction.

:dutchSteps:	
    integer, optional

    Number of steps within the dutch part of the insider auction.

    Possible values are [1; 99]. Defaul value is 99.
