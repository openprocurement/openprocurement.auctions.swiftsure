.. _tutorial:


.. index:: Auction

Creating auction
----------------

The auction is created automaticaly by bot. You can see this in owner field when retrieving auction by its `id`:

.. include:: tutorial/retrieve-auction-json-data.http
   :code:

Note that auction is initialy in `pending.activation` status. Also note that lot created before has `access` section which contains a ``transfer`` key. It is used to retrieve procedure ownership from bot in order to activate auction further.

Let's see what listing of auctions reveals us:

.. include:: tutorial/initial-auction-listing.http
   :code:

We do see the auction's internal `id` (that can be used to construct full URL by prepending `https://lb.api-sandbox.ea2.openprocurement.net/api/2.3/auctions/`) and its `dateModified` datestamp.

Enquiries
---------

When auction is in `active.tendering` status, interested parties can ask questions:

.. include:: tutorial/ask-question.http
   :code:

Organizer can answer them:

.. include:: tutorial/answer-question.http
   :code:

And one can retrieve the question list:

.. include:: tutorial/list-question.http
   :code:

Or an individual answer:

.. include:: tutorial/get-answer.http
   :code:


.. _1_submitted_proposal:

1 submitted proposal
~~~~~~~~~~~~~~~~~~~~

Activate procedure
------------------
To be able to register a bid we need to switch procedure to active.tendering status. We can to do this by changing procedure owner. First we need to create a `Transfer` object:

.. include:: tutorial/create_transfer.http
   :code:

`Transfer` object contains new access ``token`` and new ``transfer`` token. They replace old auctions access ``token`` and lots ``transfer`` when we will change ownership of procedure.

`Transfer` can be retrieved by `id`:

.. include:: tutorial/retrieve_transfer.http
   :code:

To change auctions ownership broker should send POST request to appropriate `/auctions/<id>/` with `data` section containing ``id`` of Transfer and ``transfer`` token received when creating a lot:

.. include:: tutorial/transfer_token.http
   :code:

You can see that now you are owner of auction and status have changed to 'active.tendering'

.. index:: Bidding

Registering bid
---------------

Bidder can register a bid in `draft` status:

.. include:: tutorial/register-bidder.http
   :code:

And activate a bid:

.. include:: tutorial/activate-bidder.http
   :code:

Then upload proposal document:

.. include:: tutorial/upload-bid-proposal.http
   :code:

It is possible to check the uploaded documents:

.. include:: tutorial/bidder-documents.http
   :code:

If only one bid was registered then procedure autoimaticaly change status to `active.qualification` and one award in `pending.admission` will be generated. We cen view this award:

.. include:: tutorial/get-award.http
   :code:

Then broker should upload admission protocol:

.. include:: tutorial/upload-admission-protocol.http
   :code:

And then you can update it with details:

.. include:: tutorial/patch-admission-protocol.http
   :code:

After uploading of the admission protocol you are able to update award status to pending:

.. include:: tutorial/update-award-to-pending.http
   :code:

Next step is to upload auction protocol:

.. include:: tutorial/bidder-auction-protocol.http
   :code:

We can update some of its fields:

.. include:: tutorial/update-bidder-auction-protocol.http
   :code:

And finally activate award:

.. include:: tutorial/confirm-qualification.http
   :code:

Now we can find out that our auction has a contract with its id:

.. include:: tutorial/get-contract.http
   :code:

Lets upload contract document:

.. include:: tutorial/auction-contract-upload-document.http
   :code:

And sign it:

.. include:: tutorial/signing-contract.http
   :code:

To activate a contract one more POST request should be done:

.. include:: tutorial/activate-contract.http
   :code:

You can see that our auction is now in `complete` status:

.. include:: tutorial/check-contract-status.http
   :code:

.. index:: 2_submitted_proposals_or_more, Confirming_qualification, Contract_prolongation, Candidate_disqualification

.. _2_submitted_proposals_or_more:

2 submitted proposals or more
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We have auction owned by us. Lets try to register first bidder in `draft` status:

.. include:: tutorial/2bidders-register-first-bidder.http
   :code:

Activate it:

.. include:: tutorial/2bidders-activate-bidder.http
   :code:

Upload proposal:

.. include:: tutorial/2bidders-upload-bid-proposal.http
   :code:

For the best effect (biggest economy) auction should have multiple bidders registered:

.. include:: tutorial/register-2nd-bidder.http
   :code:

Activate second bidder:

.. include:: tutorial/2bidders-activate-second-bidder.http
   :code:

Upload second bidder proposal:

.. include:: tutorial/2bidders-upload-second-bid-proposal.http
   :code:

Now procedure is ready for auction stage.

Auction
~~~~~~~

 After auction is scheduled anybody can visit it to watch. The auction can be reached at `Auction.auctionUrl`:

.. include:: tutorial/auction-url.http
   :code:

And bidders can find out their participation URLs via their bids:

.. include:: tutorial/bidder-participation-url.http
   :code:

See the `Bid.participationUrl` in the response. Similar, but different, URL can be retrieved for other participants:

.. include:: tutorial/bidder2-participation-url.http
   :code:


After the competitive auction two `awards` are created:

.. include:: qualification/awards-get.http
   :code:

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

It is the organizer's duty to upload and confirm the protocol, as well as to switch the award to `active` status:

.. include:: qualification/award-pending-upload.http
   :code:

Also auction protocol can be modified:

.. include:: qualification/patch-award.http
   :code:

And confirm qualification:

.. include:: qualification/confirm-qualification-2bids.http
   :code:

.. include:: qualification/award-pending-unsuccessful.http
   :code:

 Otherwise, the award will automatically become `unsuccessful`


Disqualification of a candidate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In case of manual disqualification, the organizer has to upload file with cancellation reason:


.. include:: qualification/award-active-unsuccessful-upload.http
  :code:

Update rejection protocol:

.. include:: qualification/patch-award-active-unsuccessful.http
  :code:

And disqualify candidate:

.. include:: qualification/award-pending-unsuccessful.http
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

Get contract id:

.. include:: tutorial/get-contract-2bids.http
   :code:

You can upload contract documents. Let's upload contract document:

.. include:: tutorial/auction-contract-upload-document-2bids.http
   :code:

`201 Created` response code and `Location` header confirm that document has been added.

Let's see the list of contract documents:

.. include:: tutorial/auction-contract-get-documents-2bids.http
   :code:

We can add another contract document:

.. include:: tutorial/auction-contract-upload-second-document-2bids.http
   :code:

`201 Created` response code and `Location` header confirm that the second document has been uploaded.

Let's see the list of all added contract documents:

.. include:: tutorial/auction-contract-get-documents-again-2bids.http
   :code:


Contract registration
~~~~~~~~~~~~~~~~~~~~~

There is a possibility to set custom contract signature date.
If the date is not set it will be generated on contract registration.
You can register contract:

.. include:: tutorial/auction-contract-sign-2bids.http
   :code:

Sign contract:

.. include:: tutorial/signing-contract-2bids.http
   :code:

Activate contract:

.. include:: tutorial/activate-contract-2bids.http
   :code:

Check status:

.. include:: tutorial/check-contract-status-2bids.http
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
