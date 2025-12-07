from __future__ import annotations

from typing import Any, Dict, List, Optional

from aiogram.fsm.context import FSMContext


async def get_stack(state: FSMContext) -> List[Dict[str, Any]]:
    data = await state.get_data()
    return list(data.get("nav_stack", []))


async def set_stack(state: FSMContext, stack: List[Dict[str, Any]]) -> None:
    await state.update_data(nav_stack=stack)


async def push(state: FSMContext, name: str, payload: Optional[Dict[str, Any]] = None) -> None:
    stack = await get_stack(state)
    stack.append({"name": name, "payload": (payload or {})})
    await set_stack(state, stack)


async def pop(state: FSMContext) -> Dict[str, Any]:
    stack = await get_stack(state)
    if stack:
        stack.pop()
    await set_stack(state, stack)
    return stack[-1] if stack else {"name": "main", "payload": {}}


async def current(state: FSMContext) -> Dict[str, Any]:
    stack = await get_stack(state)
    return stack[-1] if stack else {"name": "main", "payload": {}}


