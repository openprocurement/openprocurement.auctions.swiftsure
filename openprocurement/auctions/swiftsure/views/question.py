# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    apply_patch,
    context_unpack,
    get_now,
    json_view,
    opresource,
    save_auction,
)
from openprocurement.auctions.core.validation import (
    validate_question_data,
    validate_patch_question_data,
)
from openprocurement.auctions.core.views.mixins import AuctionQuestionResource


@opresource(name='swiftsure:Auction Questions',
            collection_path='/auctions/{auction_id}/questions',
            path='/auctions/{auction_id}/questions/{question_id}',
            auctionsprocurementMethodType="swiftsure",
            description="Auction questions")
class AuctionQuestionResource(AuctionQuestionResource):

    @json_view(content_type="application/json", validators=(validate_question_data,), permission='create_question')
    def collection_post(self):
        """Post a question
        """
        auction = self.request.validated['auction']
        if (
            auction.status != 'active.tendering'
            or get_now() < auction.enquiryPeriod.startDate
            or get_now() > auction.enquiryPeriod.endDate
        ):
            self.request.errors.add('body', 'data', 'Can add question only in enquiryPeriod')
            self.request.errors.status = 403
            return
        question = self.request.validated['question']
        if any([i.status != 'active' for i in auction.lots if i.id == question.relatedItem]):
            self.request.errors.add('body', 'data', 'Can add question only in active lot status')
            self.request.errors.status = 403
            return
        auction.questions.append(question)
        if save_auction(self.request):
            self.LOGGER.info(
                'Created auction question {}'.format(question.id),
                extra=context_unpack(
                    self.request,
                    {'MESSAGE_ID': 'auction_question_create'},
                    {'question_id': question.id}))
            self.request.response.status = 201
            route = self.request.matched_route.name.replace("collection_", "")
            self.request.response.headers['Location'] = self.request.current_route_url(
                _route_name=route, question_id=question.id, _query={}
            )
            return {'data': question.serialize("view")}

    @json_view(content_type="application/json", permission='edit_auction', validators=(validate_patch_question_data,))
    def patch(self):
        """Post an Answer
        """
        auction = self.request.validated['auction']
        if auction.status != 'active.tendering':
            self.request.errors.add(
                'body',
                'data',
                'Can\'t update question in current ({}) auction status'.format(auction.status))
            self.request.errors.status = 403
            return
        if any([i.status != 'active' for i in auction.lots if i.id == self.request.context.relatedItem]):
            self.request.errors.add('body', 'data', 'Can update question only in active lot status')
            self.request.errors.status = 403
            return
        if apply_patch(self.request, src=self.request.context.serialize()):
            self.LOGGER.info(
                'Updated auction question {}'.format(self.request.context.id),
                extra=context_unpack(
                    self.request,
                    {'MESSAGE_ID': 'auction_question_patch'}))
            return {'data': self.request.context.serialize(auction.status)}
