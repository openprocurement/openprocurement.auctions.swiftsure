.. _tutorial:

Creating auction
----------------

As long as lot's rectificationPeriod expires, a procedure is being created automatically:

.. include:: tutorial/retrieve-auction-json-data.http
   :code:

Note that the procedure initially receives `pending.activation` status.

Let's see what listing of auctions reveals us:

.. include:: tutorial/initial-auction-listing.http
   :code:

We do see the auction's internal `id` (that can be used to construct full URL `https://lb.api-sandbox.ea2.openprocurement.net/api/2.3/auctions/`) and its `dateModified` datestamp.

Procedure activation
------------------

The initial version of the procedure comes with `concierge` as an owner, pointing an entity whom the procedure has been originally created by.

You have been given the `access_transfer` key while creating a lot. Consider that `access_transfer` is used to retrieve procedure ownership so that to activate the process.

In order to switch the procedure to `active.tendering` a `Transfer` object has to be created first:

.. include:: tutorial/create_transfer.http
   :code:

`Transfer` object contains new `access_token` & `access_transfer`. Those are the ones to replace the previous data within the `access` while changing the ownership of a procedure.

`Transfer` can be retrieved by `id`:

.. include:: tutorial/retrieve_transfer.http
   :code:

For the procedure ownership to be changed, you should send POST request to the appropriate `/auctions/<id>/` with `data` section containing `id` of the `Transfer` and `access_transfer` received while creating the lot:

.. include:: tutorial/transfer_token.http
   :code:

You should also switch the procedure to `active.tendering`.

...........

Success! Now we can see that new object has changed its `owner` and `status`.

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
-------

 After auction is scheduled anybody can visit it to watch. The auction can be reached at `Auction.auctionUrl`:

.. include:: tutorial/auction-url.http
   :code:

And bidders can find out their participation URLs via their bids:

.. include:: tutorial/bidder-participation-url.http
   :code:

See the `Bid.participationUrl` in the response. Similar, but different, URL can be retrieved for other participants:

.. include:: tutorial/bidder2-participation-url.http
   :code:

1 Submitted Proposal
--------------------

If only one bid has been registered the procedure automaticaly changes its status to `active.qualification`. The award is being created in `pending.admission` status:

.. include:: tutorial/get-award.http
   :code:

Pay attention to the admissionPeriod generated. For the process to move forward, you have to upload an admission protocol (`documentType: admissionProtocol`) in time (up to `admissionPeriod.endDate`):

.. include:: tutorial/upload-admission-protocol.http
   :code:

And update it with more details:

.. include:: tutorial/patch-admission-protocol.http
   :code:

With the document being uploaded you have to switch the award to `pending` status:

.. include:: tutorial/update-award-to-pending.http
   :code:

You can also reject working with a bidder by uploading a document (`rejectionProtocol` or `act`) and switching the award to `unsuccessful`.

With the award being switched to `pending`, two more periods are being generated. These are `verificationPeriod` & `signingPeriod`:

The first thing to be done is `auctionProtocol` uploading:

.. include:: tutorial/bidder-auction-protocol.http
   :code:

We can also update it with more details:

.. include:: tutorial/update-bidder-auction-protocol.http
   :code:

With the document being uploaded you have to switch the award to `active` status:

.. include:: tutorial/confirm-qualification.http
   :code:

Now you can see that the `contract` object has been created:

.. include:: tutorial/get-contract.http
   :code:

To complete the process you have to upload a document (`contractSigned`):

.. include:: tutorial/auction-contract-upload-document.http
   :code:

Setting the correct `documentType`:

.. include:: tutorial/signing-contract.http
   :code:

Note that `dateSigned` has to be mentioned as well.

To activate a contract one more POST request should be done:

.. include:: tutorial/activate-contract.http
   :code:

And finally the procedure is in `complete` status:

.. include:: tutorial/check-contract-status.http
   :code:

2 submitted proposals or more
-----------------------------

After the competitive auction two `awards` are created:

.. include:: qualification/awards-get.http
   :code:

* for the first candidate (a participant that has submitted the highest valid bid at the auction) - initially has a `pending` status and awaits auction protocol to be uploaded by the organizer;

* for the second candidate (a participant that has submitted the second highest valid bid at the auction)- initially has a `pending.waiting` status.

There are two more scenarios that can happen after the competitive auction:
 
* If the two highest bidders have invalid bids (lower than auction starting price + minimal step), the awards will not be created at all, and the qualification procedure will automatically receive the `unsuccessful` status. 

* If the second highest bidder has a bid that is less than the starting price + minimal step, two awards are created, with one of them receiving a pending status and undergoing the qualification procedure, and the other (with an invalid bid) automatically becoming `unsuccessful`.

Refusal of waiting by another participant
-----------------------------------------

The second candidate (participant that has submitted the second highest valid bid at the auction) can refuse to wait for the disqualification of the first candidate:

.. include:: qualification/award-waiting-cancel.http
  :code:

Disqualification of a candidate
-------------------------------

In case of a manual disqualification, the organizer has to upload file with cancellation reason:

.. include:: qualification/award-active-unsuccessful-upload.http
  :code:

Update rejection protocol:

.. include:: qualification/patch-award-active-unsuccessful.http
  :code:

And disqualify candidate:

.. include:: qualification/award-pending-unsuccessful.http
  :code:

