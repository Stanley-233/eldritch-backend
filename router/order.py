import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from model.message import Order, Report
from model.user import User, UserGroup
from util.engine import get_session

order_router = APIRouter()

@order_router.get("/order/create_user={username}/open")
async def get_orders_open(username: str, session: Session = Depends(get_session)):
    """获取指定用户创建的open工单"""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    orders = session.exec(
        select(Order).where(Order.c_by_username == username)
    ).all()
    orders_list = [
        {
            "order_id": order.order_id,
            "title": order.title,
            "content": order.content,
            "created_by": order.c_by_username,
            "created_at": order.created_at,
            "status": order.status
        } for order in orders
    ]
    orders_list = [
        order for order in orders_list if order["status"] == "open"
    ]
    return orders_list

@order_router.get("/order/create_user={username}/reject")
async def get_orders_reject(username: str, session: Session = Depends(get_session)):
    """获取指定用户创建被拒绝工单"""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    orders = session.exec(
        select(Order).where(Order.c_by_username == username)
    ).all()
    orders_list = [
        {
            "order_id": order.order_id,
            "title": order.title,
            "content": order.content,
            "created_by": order.c_by_username,
            "created_at": order.created_at,
            "status": order.status
        } for order in orders
    ]
    orders_list = [
        order for order in orders_list if order["status"] == "reject"
    ]
    return orders_list

@order_router.get("/order/create_user={username}/closed")
async def get_orders_closed(username: str, session: Session = Depends(get_session)):
    """获取指定用户创建已关闭工单"""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    orders = session.exec(
        select(Order).where(Order.c_by_username == username)
    ).all()
    orders_list = [
        {
            "order_id": order.order_id,
            "title": order.title,
            "content": order.content,
            "created_by": order.c_by_username,
            "created_at": order.created_at,
            "status": order.status
        } for order in orders
    ]
    orders_list = [
        order for order in orders_list if order["status"] == "closed"
    ]
    return orders_list

@order_router.get("/order/assigned_user={username}/open")
async def get_orders_assigned_open(username: str, session: Session = Depends(get_session)):
    """获取指定用户被分配且未处理的工单"""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    groups = user.groups
    orders_list = []
    for group in groups:
        orders = group.orders
        orders_list.extend([
            {
                "order_id": order.order_id,
                "title": order.title,
                "content": order.content,
                "created_by": order.c_by_username,
                "created_at": order.created_at,
                "status": order.status
            } for order in orders
        ])
    orders_list = [
        order for order in orders_list if order["status"] == "open"
    ]
    # 过滤掉重复的工单
    final_orders = list({order.message_id: order for order in orders_list}.values())
    return final_orders

@order_router.get("/order/assigned_user={username}/reject")
async def get_orders_assigned_reject(username: str, session: Session = Depends(get_session)):
    """获取指定用户被分配且已拒绝的工单"""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    groups = user.groups
    orders_list = []
    for group in groups:
        orders = group.orders
        orders_list.extend([
            {
                "order_id": order.order_id,
                "title": order.title,
                "content": order.content,
                "created_by": order.c_by_username,
                "created_at": order.created_at,
                "status": order.status
            } for order in orders
        ])
    orders_list = [
        order for order in orders_list if order["status"] == "reject"
    ]
    # 过滤掉重复的工单
    final_orders = list({order.message_id: order for order in orders_list}.values())
    return final_orders

@order_router.get("/order/assigned_user={username}/closed")
async def get_orders_assigned_closed(username: str, session: Session = Depends(get_session)):
    """获取指定用户被分配且已关闭的工单"""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    groups = user.groups
    orders_list = []
    for group in groups:
        orders = group.orders
        orders_list.extend([
            {
                "order_id": order.order_id,
                "title": order.title,
                "content": order.content,
                "created_by": order.c_by_username,
                "created_at": order.created_at,
                "status": order.status
            } for order in orders
        ])
    orders_list = [
        order for order in orders_list if order["status"] == "closed"
    ]
    # 过滤掉重复的工单
    final_orders = list({order.message_id: order for order in orders_list}.values())
    return final_orders

@order_router.get("/order/order_id={order_id}/report")
async def get_report(order_id: int, session: Session = Depends(get_session)):
    """获取指定工单绑定的报告"""
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.report is None:
        raise HTTPException(status_code=401, detail="Report not found for this order")
    report = {
        "report_id": order.report.report_id,
        "content": order.report.content,
        "created_by": order.report.c_by_username,
        "created_at": order.report.created_at,
        "status": order.report.status
    }
    return report

class OrderRequest(BaseModel):
    """工单创建请求体"""
    title: str
    content: str
    assigned_groups: List[int]
    created_by: str

@order_router.post("/order/create")
async def create_order(request: OrderRequest, session: Session = Depends(get_session)):
    """创建工单"""
    user = session.get(User, request.created_by)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    assigned_groups = []
    for group_id in request.assigned_groups:
        group = session.get(UserGroup, group_id)
        if not group:
            raise HTTPException(status_code=404, detail=f"No such group with id {group_id} found")
        assigned_groups.append(group)

    new_order = Order(
        title=request.title,
        content=request.content,
        c_by_username=user.username,
        created_by=user,
        assigned_groups=assigned_groups,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    return {"message": "Order created successfully", "order_id": new_order.order_id}

class ReportRequest(BaseModel):
    order_id: int
    content: str
    status: str = "closed"
    created_by: str

@order_router.post("/order/report/create")
async def create_report(request: ReportRequest, session: Session = Depends(get_session)):
    """创建工单反馈"""
    user = session.get(User, request.created_by)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order = session.get(Order, request.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    new_report = Report(
        content=request.content,
        c_by_username=user.username,
        created_by=user,
        created_at=datetime.datetime.now(),
        order_id=order.order_id,
        order=order
    )
    order.status = request.status
    session.add(new_report)
    session.add(order)
    session.commit()
    session.refresh(new_report)

    return {"message": "Report created successfully", "report_id": new_report.report_id}

