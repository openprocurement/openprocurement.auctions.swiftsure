Overview
========

openprocurement.auctions.sellout.english contains documentaion regarding open ascending price auctions within the Small-Scale Privatization process.

Type of the given procedure:

* sellout.english 



Features
--------

* No need to specify enquiries period (there is no *active.enquiries* status), since it overlaps with *active.tendering* period.
* For the process to start, owner should switch the procedure from *pending.activation* status to *active.tendering*.
* During *active.tendering* period participants can ask questions, submit proposals, and upload documents.
* Organizer is not allowed to set any changes within the procedure.
* The given procurementMethodType is used during the first and second phase of the Small-Scale Privatization process.
* For the procedure to become complete only 1 proposal is needed. 
* In case of a one proposal has been submitted, the auction itself will be ommitted.
* Considering the number of proposals submitted, the Awarding process varies. 

Conventions
-----------

API accepts `JSON <http://json.org/>`_ or form-encoded content in
requests.  It returns JSON content in all of its responses, including
errors.  Only the UTF-8 character encoding is supported for both requests
and responses.

All API POST and PUT requests expect a top-level object with a single
element in it named `data`.  Successful responses will mirror this format. 
The data element should itself be an object, containing the parameters for
the request.  In the case of creating a new auction, these are the fields we
want to set on the auction itself.

If the request was successful, we will get a response code of `201`
indicating the object was created.  That response will have a data field at
its top level, which will contain complete information on the new auction,
including its ID.

If something went wrong during the request, we'll get a different status
code and the JSON returned will have an `errors` field at the top level
containing a list of problems.  We look at the first one and print out its
message.

Project status
--------------

The project has pre alpha status.

The source repository for this project is on GitHub: https://github.com/openprocurement/openprocurement.auctions.swiftsure

You can leave feedback by raising a new issue on the `issue tracker
<https://github.com/openprocurement/openprocurement.auctions.swiftsure/issues>`_ (GitHub
registration necessary).  

Documentation of related packages
---------------------------------

* `OpenProcurement API <http://api-docs.openprocurement.org/en/latest/>`_
* `Assets Registry <http://assetsbounce.api-docs.registry.ea2.openprocurement.io/en/latest/>`_
* `Lots Registry <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/>`_

API stability
-------------

API is relatively stable. The changes in the API are communicated via `Open Procurement API
<https://groups.google.com/group/open-procurement-api>`_ maillist and ProZorro.Sale Slack chats.

Change log
----------

0.1
~~~

Released: not released


Next steps
----------
You might find it helpful to look at the :ref:`tutorial`.
