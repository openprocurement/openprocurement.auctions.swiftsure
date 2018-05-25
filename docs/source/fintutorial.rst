.. _fintutorial:

Fin. Tutorial
=============

Tutorial for the `sellout.english` procedure.

Creating auction
----------------

The auction is created with the data set (only required properties) provided within the Lots Registry:

.......................

Note that auction is created with `pending.activation` status.

Let's access the URL of the created object:

...............................

Let's see what listing of auctions reveals us:

...................

We do see the auction's internal `id` (that can be used to construct full URL by prepending `https://lb.api-sandbox.ea2.openprocurement.net/api/2.3/auctions/`) and its `dateModified` datestamp.

.. index:: Bidding

Registering bid
---------------

Bidder can register a bid in `draft` status. Bidder must specify ``UA-FIN`` value for the `additionalIdentifiers` parameter.

.. include:: tutorial/register-finbidder.http
   :code:

And activate a bid:

.. include:: tutorial/activate-finbidder.http
   :code:

It is possible to check the uploaded documents:

.. include:: tutorial/finbidder-documents.http
   :code:

For the best effect (biggest economy) auction should have multiple bidders registered:

.. include:: tutorial/register-2nd-finbidder.http
   :code:
