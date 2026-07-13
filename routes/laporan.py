import csv
from io import StringIO

from flask import Blueprint, Response, render_template, request

from models.database_model import Laporan
from routes.auth import role_required

laporan_bp = Blueprint("laporan", __name__)


@laporan_bp.route("/laporan")
@role_required("admin")
def laporan():
    query = Laporan.query
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    if start_date:
        query = query.filter(Laporan.tanggal >= start_date)
    if end_date:
        query = query.filter(Laporan.tanggal <= end_date)

    reports = query.order_by(Laporan.tanggal.desc()).all()
    return render_template("laporan.html", reports=reports, start_date=start_date, end_date=end_date)


@laporan_bp.route("/laporan/export")
@role_required("admin")
def export_laporan():
    reports = Laporan.query.order_by(Laporan.tanggal.desc()).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["tanggal", "total_sampah", "jumlah_pengambilan", "keterangan"])
    for report in reports:
        writer.writerow([report.tanggal, report.total_sampah, report.jumlah_pengambilan, report.keterangan])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=laporan_smartwaste.csv"},
    )
