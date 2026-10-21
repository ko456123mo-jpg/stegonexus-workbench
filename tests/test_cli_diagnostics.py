"""انحدار: الواجهة النصية --diagnostics كانت تنهار بـ KeyError.

``ToolStatus.as_dict()`` صار يعرض ``available``/``classification`` فقط، بينما
ظلّ ``run_diagnostics`` يقرأ مفتاح ``status`` غير الموجود — فيطبع العنوان ثم
يسقط بـ KeyError قبل أول صف. الواجهة الرسومية كانت تعمل (تقرأ المفاتيح الصحيحة)
فلم يلاحظ أحد أن مسار الـCLI الموثّق معطّل.
"""
from __future__ import annotations

from app.services.tool_health import ToolStatus


def test_diagnostics_prints_a_row_per_tracked_tool(capsys) -> None:
    from app.gui.app import run_diagnostics

    assert run_diagnostics() == 0
    out = capsys.readouterr().out
    assert "tool health" in out
    # كل صف يحمل تصنيفاً معروفاً — لا KeyError ولا صف فارغ
    assert any(label in out for label in ("AVAILABLE", "REFERENCE", "MISSING"))


def test_as_dict_and_row_labels_stay_in_sync() -> None:
    """حارس ضد تكرار العلة: أي مفتاح يقرأه العرض يجب أن يُنتجه as_dict()."""
    row = ToolStatus(name="exiftool", kind="binary", available=True).as_dict()
    assert "available" in row and "classification" in row
    assert "status" not in row  # المفتاح القديم أُزيل — لا تعتمد عليه
