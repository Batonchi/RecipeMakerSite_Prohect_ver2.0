import asyncio
import sys

import uvicorn
from fastapi import FastAPI, Request
from sqladmin import Admin, ModelView, expose
from starlette.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.clients.model import (
    BankClient, MobileClient, MobileBuild, BankTransactions,
    MarketPlaceDelivery, EcosystemMapping
)
from app.support.model import Complaint
from base.database import async_session_maker, engine
from app.support.service import BankComplaintService

app = FastAPI()
app.mount('/static', StaticFiles(directory='app/view/static'))
admin = Admin(app, engine, base_url="/admin",
              templates_dir="templates", )
admin.templates.env.globals["admin_extra_css"] = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
]


class ComplaintAdmin(ModelView, model=Complaint):
    name = "Жалоба"
    name_plural = "Жалобы"
    icon = "fa-solid fa-bolt"

    column_list = [Complaint.id, Complaint.user_id, Complaint.text]
    column_searchable_list = [Complaint.user_id]
    form_columns = [Complaint.user_id, Complaint.text]


class BankClientAdmin(ModelView, model=BankClient):
    column_list = [BankClient.client_id, BankClient.account, BankClient.phone, BankClient.fio]
    column_searchable_list = [BankClient.client_id, BankClient.phone]
    column_sortable_list = [BankClient.client_id]
    form_columns = [BankClient.client_id, BankClient.account, BankClient.phone, BankClient.fio]


class MobileClientAdmin(ModelView, model=MobileClient):
    column_list = [MobileClient.client_id, MobileClient.phone, MobileClient.fio, MobileClient.address]
    column_searchable_list = [MobileClient.client_id, MobileClient.phone]
    form_columns = [MobileClient.client_id, MobileClient.phone, MobileClient.fio, MobileClient.address]


class MobileBuildAdmin(ModelView, model=MobileBuild):
    column_list = [MobileBuild.id, MobileBuild.event_date, MobileBuild.from_call, MobileBuild.to_call,
                   MobileBuild.duration_sec]
    column_searchable_list = [MobileBuild.from_call, MobileBuild.to_call]
    form_columns = [MobileBuild.event_date, MobileBuild.from_call, MobileBuild.to_call, MobileBuild.duration_sec]


class BankTransactionsAdmin(ModelView, model=BankTransactions):
    column_list = [BankTransactions.id, BankTransactions.event_date, BankTransactions.account_out,
                   BankTransactions.account_in, BankTransactions.value]
    column_searchable_list = [BankTransactions.account_out, BankTransactions.account_in]
    form_columns = [BankTransactions.event_date, BankTransactions.account_out, BankTransactions.account_in,
                    BankTransactions.value]


class MarketPlaceDeliveryAdmin(ModelView, model=MarketPlaceDelivery):
    column_list = [MarketPlaceDelivery.id, MarketPlaceDelivery.event_date, MarketPlaceDelivery.user_id,
                   MarketPlaceDelivery.contact_fio, MarketPlaceDelivery.contact_phone, MarketPlaceDelivery.address]
    column_searchable_list = [MarketPlaceDelivery.user_id, MarketPlaceDelivery.contact_phone]
    form_columns = [MarketPlaceDelivery.event_date, MarketPlaceDelivery.user_id, MarketPlaceDelivery.contact_fio,
                    MarketPlaceDelivery.contact_phone, MarketPlaceDelivery.address]


class EcosystemMappingAdmin(ModelView, model=EcosystemMapping):
    column_list = [EcosystemMapping.id, EcosystemMapping.bank_id, EcosystemMapping.mobile_user_id,
                   EcosystemMapping.market_place_user_id]
    column_searchable_list = [EcosystemMapping.bank_id, EcosystemMapping.mobile_user_id]
    form_columns = [EcosystemMapping.bank_id, EcosystemMapping.mobile_user_id, EcosystemMapping.market_place_user_id]


admin.add_view(BankClientAdmin)
admin.add_view(MobileClientAdmin)
admin.add_view(MobileBuildAdmin)
admin.add_view(BankTransactionsAdmin)
admin.add_view(MarketPlaceDeliveryAdmin)
admin.add_view(EcosystemMappingAdmin)
admin.add_view(ComplaintAdmin)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run(app, host="localhost", port=8000)
