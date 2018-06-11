.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Document, Attachment, File, Notice, Bidding Documents, Technical Specifications, Evaluation Criteria, Clarifications

.. _Document:

Document
========

Schema
------

:id:
    string, auto-generated

:documentType:
    string, required

    Possible values for :ref:`auction`

    * `notice` - **Auction notice**

      The formal notice that gives details of an auction. This may be a link to a downloadable document, to a web page, or to an official gazette in which the notice is contained.

    * `technicalSpecifications` - **Technical Specifications**

      Detailed technical information about goods or services to be provided.

    * `evaluationCriteria` - **Evaluation Criteria**

      Information about how bids will be evaluated.

    * `clarifications` - **Clarifications to bidders questions**

      Including replies to issues raised in pre-bid conferences.

    * `bidders` - **Information on bidders**

      Information on bidders or participants, their validation documents and any procedural exemptions for which they qualify.

    * `virtualDataRoom` - **Virtual Data Room** (available only for the `dgfFinancialAssets` procedure, see :ref:`fintutorial`)

    * `illustration` - **Illustrations**

    * `x_PublicAssetCertificate` - **Public Asset Certificate**

      Information about the auction. It is a link to the Public Asset Certificate.

    * `x_presentation` - **Presentation**

      Presentation about an asset that is being sold.

    * `x_nda` - **Non-disclosure Agreement (NDA)**

      A non-disclosure agreement between a participant and a bank/Deposit Guarantee Fund.

    * `x_PlatformLegalDetails` - **Platform Legal Details**

      Place and application forms for participation in the auction as well as bank details for transferring guarantee deposits.

    * `x_dgfAssetFamiliarization` - **Asset Familiarization**

      Goods examination procedure rules / Asset familiarization procedure in data room. Contains information on where and when a given document can be examined offline.


    Possible values for :ref:`award`


    * `winningBid` - **Winning Bid**

    Possible values for :ref:`contract`


    * `notice` - **Contract notice**

      The formal notice that gives details of a contract being signed and valid to start implementation. This may be a link to a downloadable document, to a web page, or to an official gazette in which the notice is contained.

    * `contractSigned` - **Signed Contract**

    * `contractAnnexe` - **Annexes to the Contract**


    Possible values for :ref:`bid`


    * `commercialProposal` - **Сommercial proposal**

    * `qualificationDocuments` - **Qualification documents**

    * `eligibilityDocuments` - **Eligibility documents**

    * `financialLicense` - **License** 

    * `auctionProtocol` - **Auction protocol**

        Auction protocol describes all participants and determines the candidate (participant that has submitted the highest bid proposal during the auction).


:title:
    string, multilingual, required

    |ocdsDescription|
    The document title.

:description:
    string, multilingual, optional

    |ocdsDescription|
    A short description of the document. In the event the document is not accessible online, the description field can be used to describe arrangements for obtaining a copy of the document.

:index:
    integer, optional

    Sorting (display order) parameter used for illustrations. The smaller number is, the higher illustration is in the sorting. If index is not specified, illustration will be displayed the last. If two illustrations have the same index, they will be sorted depending on their publishing date.

:format:
    string, optional

    |ocdsDescription|
    The format of the document taken from the `IANA Media Types code list <http://www.iana.org/assignments/media-types/>`_, with the addition of one extra value for 'offline/print', used when this document entry is being used to describe the offline publication of a document.

:url:
    string, auto-generated

    |ocdsDescription|
    Direct link to the document or attachment.

:datePublished:
    string, :ref:`date`, auto-generated

    |ocdsDescription|
    The date on which the document was first published.

:dateModified:
    string, :ref:`date`, auto-generated

    |ocdsDescription|
    Date that the document was last modified

:language:
    string, optional

    |ocdsDescription|
    Specifies the language of the linked document using either two-digit `ISO 639-1 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_, or extended `BCP47 language tags <http://www.w3.org/International/articles/language-tags/>`_.

:documentOf:
    string, required

    Possible values are:

    * `auction`
    * `item`

:relatedItem:
    string, optional

    ID of related :ref:`item`.
