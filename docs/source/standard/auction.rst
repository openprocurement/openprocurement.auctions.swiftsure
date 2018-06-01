.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Auction, Auction
.. _auction:

Auction
=======

Schema
------

:id:
  string, auto-generated, read-only
  
:auctionID:
  string, auto-generated, read-only

  The auction identifier to refer to in "paper" documentation. 

  |ocdsDescription|
  AuctionID should always be the same as the OCID. It is included to make the flattened data structure more convenient.
  
:merchandisingObject:
  string, auto-generated, read-only

  Originates from `lots.id`.
  
  Lot's id.

:title:
  string, multilingual, required

  Originates from `lots.title`.

  The name of the auction, displayed in listings. 
 
:description:
  string, multilingual, required

  Originates from `lots.description`.
  
  Detailed auction description. 
  
:procurementMethodType:
  string, auto-generated, required
  
  Originates from `lots.auctions.procurementMethodType`.
  
  Type of the procedure within the auction announcement. The only type is english. 

:procurementMethodDetails:
  string, auto-generated
  
  Originates from `lots.auctions.procurementMethodDetails`.

  Parameter that accelerates auction periods. Set quick, accelerator=1440 as text value for procurementMethodDetails for the time frames to be reduced in 1440 times.

:submissionMethodDetails:
  
  string, auto-generated
  
  Originates from `lots.auctions.submissionMethodDetails`.

  Parameter that works only with mode = “test” and speeds up auction start date.

  Possible values are:

  * -`quick(mode:no-auction)`;
  * -`quick(mode:fast-forward)`.


:procuringEntity:
  :ref:`ProcuringEntity`, required

  Originates from `lots.lotCustodian`.
  
  Organization conducting the auction.

  |ocdsDescription|
  The entity managing the procurement, which may be different from the buyer who is paying / using the items being procured.

:tenderAttempts:
  integer, required

  Originates from `lots.auctions.tenderAttempts`.

  The number which represents what time (from 1 up to 3) procedure with a current lot takes place.

:value:
  :ref:`value`, required

  Originates from `lots.auctions.value`. 

  
  Total available budget of the 1st auction. Bids lower than ``value`` will be rejected.

  Auction.value for 2nd auction within the privatization cycle will be calculated as half of the auction.value provided.

  |ocdsDescription|
  The total estimated value of the procurement.
  
:guarantee:
  :ref:`Guarantee`, required

  Originates from `lots.auctions.guarantee`.

  Bid guarantee. Lots.auctions.guarantee for 2nd auction within the privatization cycle will be calculated automatically.

:registrationFee:
  :ref:`Guarantee`, required

  Originates from `lots.auctions.registrationFee`.
    
  Bid registration fee. Lots.auctions.registrationFee for 2nd auction within the privatization cycle will be calculated automatically.

:bankAccount:
  :ref:`Bank Account`, optional

  Originates from `lots.auctions.bankAccount`.

  Details which uniquely identify a bank account, and are used when making or receiving a payment.

:items:
  list of :ref:`item` objects, required

  Originates from `lots.items`.
  
  List that contains single item being sold.

  |ocdsDescription|
  The goods and services to be purchased, broken into line items wherever possible. Items should not be duplicated, but a quantity of 2 specified instead.

:documents:
  Array of :ref:`document` objects, optional

  |ocdsDescription|
  All documents and attachments related to the auction.

:questions:
  List of :ref:`question` objects, optional

  Questions to `procuringEntity` and answers to them.

:complaints:
  List of :ref:`complaint` objects, optional

  Complaints to auction conditions and their resolutions.

:bids:
  List of :ref:`bid` objects, optional (required when process to be succsessful)
  
  A list of all bids placed in the auction with information about participants, their proposals and other qualification documentation.

  |ocdsDescription|
  A list of all the companies who entered submissions for the auction.

:minimalStep:
  :ref:`value`, required

  Auction step (increment). Originates from `lots.auctions.minimalStep`.

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

  Period when Auction is conducted. `startDate` originates from `lots.auctions.auctionPeriod.startDate` .

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
  Array of :ref:`cancellation` objects, optional

  Contains 1 object with `active` status in case of cancelled Auction.

  The :ref:`cancellation` object describes the reason of auction cancellation and contains accompanying
  documents  if there are any.

:revisions:
  List of :ref:`revision` objects, auto-generated

  Historical changes to `Auction` object properties.
  
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

.. _Bank Account:
  
Bank Account
====

Schema
------

:description:
  string, multilingual, optional

  Additional information that has to be noted from the Organizer point.
  
  Originates from `lots.auctions.bankAccount.description`
  
:bankName:	
  string, required

  Name of the bank.
  Originates from `lots.auctions.bankAccount.bankName`
  
:accountIdentification:
  Array of :ref:`classification`, required

  Major data on the account details of the state entity selling a lot, to facilitate payments at the end of the process.

  Most frequently used are:

  * 'UA-EDR';
  * 'UA-MFO';
  * 'accountNumber'.

  Originates from `lots.auctions.bankAccount.accountIdentification`

    
