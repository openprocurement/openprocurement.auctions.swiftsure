.. _tutorial:

Tutorial
========

Exploring basic rules
---------------------

Let's try exploring the `/auctions` endpoint:

............................

Just invoking it reveals empty set.

Now let's attempt creating some auction:

......................

Error states that the only accepted Content-Type is `application/json`.

Let's satisfy the Content-type requirement:

......................

Error states that no `data` has been found in JSON body.


.. index:: Auction

Creating auction
----------------

The auction is created with the data set (only required properties) provided within the Lots Registry:

..........................

Note that auction is created with `pending.activation` status.

Let's access the URL of the created object (the `Location` header of the response):

..........................

Let's see what listing of auctions reveals us:

...........................

We do see the auction's internal `id` (that can be used to construct full URL by prepending `https://lb.api-sandbox.ea2.openprocurement.net/api/2.3/auctions/`) and its `dateModified` datestamp.

Enquiries
---------

When auction is in `active.tendering` status, interested parties can ask questions:

......................

Organizer can answer them:

........................

And one can retrieve the question list:

......................

Or an individual answer:

......................


.. index:: Bidding

Registering bid
---------------

Bidder can register a bid in `draft` status:

......................

And activate a bid:

......................

And upload proposal document:

......................

It is possible to check the uploaded documents:

......................

For the best effect (biggest economy) auction should have multiple bidders registered:

......................


.. index:: Qualification, 1_submitted_proposal, 2_submitted_proposals_or_more, Confirming_qualification, Contract_prolongation, Candidate_disqualification

Auction
-------

After auction is scheduled anybody can visit it to watch. The auction can be reached at `Auction.auctionUrl`:

......................

And bidders can find out their participation URLs via their bids:

......................

See the `Bid.participationUrl` in the response. Similar, but different, URL can be retrieved for other participants:

......................

.. _Qualification:

Qualification
-------------


.. _1_submitted_proposal:

1 submitted proposal
~~~~~~~~~~~~~~~~~~~~

.. _2_submitted_proposals_or_more:

2 submitted proposals or more
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After the competitive auction two `awards` are created:

* for the first candidate (a participant that has submitted the highest valid bid at the auction) - initially has a `pending` status and awaits auction protocol to be uploaded by the organizer;

* for the second candidate (a participant that has submitted the second highest valid bid at the auction)- initially has a `pending.waiting` status.

There are two more scenarios that can happen after the competitive auction:
 
* If the two highest bidders have invalid bids (lower than auction starting price + minimal step), the awards will not be created at all, and the qualification procedure will automatically receive the `unsuccessful` status. 

* If the second highest bidder has a bid that is less than the starting price + minimal step, two awards are created, with one of them receiving a pending status and undergoing the qualification procedure, and the other (with an invalid bid) automatically becoming `unsuccessful`.

.........................

.. _Confirming_qualification:

Confirming qualification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


The organizer **must** upload and confirm the auction protocol `auctionProtocol` and add it to the award within **4 business days after the start of the qualification procedure**. The candidate still has a possibility to upload the protocol, but it is neither mandatory, nor sufficient to move to the next status. If the auction protocol has not been uploaded before the end of `verificationPeriod`, the `award` is automatically transferred to the `unsuccessful` status.

It is the organizer's duty to upload and confirm the protocol, as well as to switch the award to `active` status.

 Otherwise, the award will automatically become `unsuccessful"`

.. _Contract_prolongation:

Contract prolongation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Organizer can prolong contract signing period by creating a prolongation object: 

.. include:: tutorial/prolongation-create.http
    :code:

For the object to be prolonged the next data has to be included:

.. include:: tutorial/prolongation-attach-document.http
    :code:

Created prolongation has status "draft" by default, so there is a need to active it:

.. include:: tutorial/prolongation-apply.http
    :code:

When a contract has been prolongated for first time, a short prolongation period (42 business days) is applied.
It's also possible to apply a long-term (132 business days) prolongation:
just create new :ref:`Prolongation` for the already prolongated :ref:`Contract`, and apply it.

.. include:: tutorial/prolongation-second-time-create.http
    :code:

.. include:: tutorial/prolongation-long-document-attach.http
    :code:

.. include:: tutorial/prolongation-long-apply.http
    :code:

.. _Candidate_disqualification:
    :code:

Disqualification of a candidate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In case of manual disqualification, the organizer has to upload file with cancellation reason:


.. include:: qualification/award-active-unsuccessful-upload.http
  :code:


And disqualify candidate:


.. include:: qualification/award-active-disqualify.http
  :code:


Within 20 business days since becoming candidate a new candidate must confirm qualification with steps described above (:ref:`Qualification`).

.. _Waiting_refusal:

Refusal of waiting by another participant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The second candidate (participant that has submitted the second highest valid bid at the auction) can refuse to wait for the disqualification of the first candidate:


.. include:: qualification/award-waiting-cancel.http
  :code:

Signing contract
----------------

The candidate has **20 business days after becoming a candidate** to conclude a contract with the bank based on the results of electronic auction.

Uploading contract documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can upload contract documents. Let's upload contract document:

.. include:: tutorial/auction-contract-upload-document.http
   :code:

`201 Created` response code and `Location` header confirm that document has been added.

Let's see the list of contract documents:

.. include:: tutorial/auction-contract-get-documents.http
   :code:

We can add another contract document:

.. include:: tutorial/auction-contract-upload-second-document.http
   :code:

`201 Created` response code and `Location` header confirm that the second document has been uploaded.

Let's see the list of all added contract documents:

.. include:: tutorial/auction-contract-get-documents-again.http
   :code:


.. _Contract_prolongation:

Contract prolongation
~~~~~~~~~~~~~~~~~~~~~

Organizer can prolongate contract signing period by creating prolongation

.. include:: tutorial/prolongation-create.http
    :code:

Prolongation must have documents attached to be prepared for activation

.. include:: tutorial/prolongation-attach-document.http
    :code:

Created prolongation has status "draft" by default, so there is a need to set status to "applied" to make it active.

.. include:: tutorial/prolongation-apply.http
    :code:

When a contract has been prolongated for first time, a short prolongation period applies.
It is equal to 42 working days. It's also possible to apply long-term (132 days) prolongation:
just create new :ref:`Prolongation` for the already prolongated :ref:`Contract`, and apply it.

.. include:: tutorial/prolongation-second-time-create.http
    :code:

.. include:: tutorial/prolongation-long-document-attach.http
    :code:

.. include:: tutorial/prolongation-long-apply.http
    :code:


Contract registration
~~~~~~~~~~~~~~~~~~~~~

There is a possibility to set custom contract signature date.
If the date is not set it will be generated on contract registration.
You can register contract:

.. include:: tutorial/auction-contract-sign.http
   :code:

Cancelling auction
------------------

Organizer can cancel auction anytime (except when auction has terminal status e.g. `unsuccesfull`, `canceled`, `complete`).

The following steps should be applied:

1. Prepare cancellation request.
2. Fill it with the protocol describing the cancellation reasons.
3. Cancel the auction with the reasons prepared.

Only the request that has been activated (3rd step above) has power to
cancel auction.  I.e.  you have to not only prepare cancellation request but
to activate it as well.

See :ref:`cancellation` data structure for details.

Preparing the cancellation request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You should pass `reason`, `status` defaults to `pending`. `id` is
autogenerated and passed in the `Location` header of response.

.. include:: tutorial/prepare-cancellation.http
   :code:


Filling cancellation with protocol and supplementary documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upload the file contents:

.. include:: tutorial/upload-cancellation-doc.http
   :code:

Change the document description and other properties:

.. include:: tutorial/patch-cancellation.http
   :code:

Upload new version of the document:

.. include:: tutorial/update-cancellation-doc.http
   :code:

Activating the request and cancelling auction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: tutorial/active-cancellation.http
   :code:
