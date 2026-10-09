import re
from reportlab.pdfgen.canvas import Canvas


class JavaScriptCanvas(Canvas):

    def __init__(self, *args, **kwargs):

        js_code = kwargs.pop("js_code", None)

        super(JavaScriptCanvas, self).__init__(
            *args,
            **kwargs
        )

        if js_code:
            self.addJS(js_code)


def inject_javascript_to_pdf(pdf_bytes: bytes, js_code: str) -> bytes:
    """
    Injects raw JavaScript code into a PDF byte stream by adding an OpenAction
    JS object and recalculating all byte offsets in the cross-reference table.
    """
    # Convert bytes to string for parsing/manipulation
    pdf_str = pdf_bytes.decode('latin-1')

    # 1. Determine the next available Object ID by inspecting existing objects
    obj_ids = [int(m.group(1)) for m in re.finditer(r'(\d+)\s+0\s+obj', pdf_str)]
    if not obj_ids:
        raise ValueError("Invalid PDF: No indirect objects found.")

    js_obj_id = max(obj_ids) + 1
    total_objects = js_obj_id + 1

    if isinstance(js_code, bytes):
        js_code = js_code.decode('utf-8')
    # Format JS code for PDF literal string (escape parenthetical characters)
    escaped_js = str(js_code).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
    # Construct the new JavaScript Action Object
    js_object_str = (
        f"{js_obj_id} 0 obj\n"
        f"<<\n/Type /Action /S /JavaScript /JS ({escaped_js})\n>>\n"
        f"endobj\n"
    )

    # 2. Locate and modify the Catalog / Root object to include /OpenAction
    catalog_match = re.search(r'(\d+)\s+0\s+obj\s*<<([^>]*?/Type\s*/Catalog[^>]*?)>>\s*endobj', pdf_str, re.DOTALL)
    if not catalog_match:
        raise ValueError("Invalid PDF: Catalog object (/Type /Catalog) not found.")

    catalog_id = catalog_match.group(1)
    catalog_body = catalog_match.group(2)

    # Inject /OpenAction into the Catalog dictionary if not already present
    if '/OpenAction' not in catalog_body:
        new_catalog_body = catalog_body.strip() + f" /OpenAction {js_obj_id} 0 R\n"
        updated_catalog_obj = f"{catalog_id} 0 obj\n<<\n{new_catalog_body}\n>>\nendobj"

        # Replace old Catalog with updated Catalog
        old_catalog_obj = catalog_match.group(0)
        pdf_str = pdf_str.replace(old_catalog_obj, updated_catalog_obj, 1)

    # 3. Append the new JS object before the xref table
    xref_pos = pdf_str.rfind('xref')
    if xref_pos == -1:
        raise ValueError("Invalid PDF: Cross-reference table ('xref') not found.")

    body_part = pdf_str[:xref_pos]
    if not body_part.endswith('\n'):
        body_part += '\n'

    pdf_with_js_body = body_part + js_object_str

    # 4. Recalculate Byte Offsets for all objects
    new_obj_offsets = {}
    obj_pattern = re.compile(r'(\d+)\s+0\s+obj')
    for match in obj_pattern.finditer(pdf_with_js_body):
        obj_id = int(match.group(1))
        offset = match.start()
        new_obj_offsets[obj_id] = offset

    # 5. Build the new Cross-Reference (xref) Table
    new_xref_offset = len(pdf_with_js_body.encode('latin-1'))

    xref_lines = [f"xref\n0 {total_objects}"]
    xref_lines.append("0000000000 65535 f ")  # Head object 0 entry

    for i in range(1, total_objects):
        offset = new_obj_offsets.get(i, 0)
        xref_lines.append(f"{offset:010d} 00000 n ")

    new_xref_str = "\n".join(xref_lines) + "\n"

    # 6. Extract original trailer content and construct updated trailer
    trailer_match = re.search(r'trailer\s*<<(.*?)>>', pdf_str, re.DOTALL)
    if not trailer_match:
        raise ValueError("Invalid PDF: Trailer dictionary not found.")

    trailer_dict_body = trailer_match.group(1)

    # Update /Size parameter in trailer
    if '/Size' in trailer_dict_body:
        trailer_dict_body = re.sub(r'/Size\s+\d+', f'/Size {total_objects}', trailer_dict_body)
    else:
        trailer_dict_body += f"\n/Size {total_objects}"

    new_trailer_str = (
        f"trailer\n<<"
        f"{trailer_dict_body}"
        f">>\n"
        f"startxref\n"
        f"{new_xref_offset}\n"
        f"%%EOF\n"
    )

    # 7. Assemble final PDF bytes
    final_pdf_str = pdf_with_js_body + new_xref_str + new_trailer_str
    return final_pdf_str.encode('latin-1')

