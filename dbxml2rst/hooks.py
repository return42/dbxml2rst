#!/usr/bin/env python3
# -*- coding: utf-8; mode: python -*-
# pylint: disable=C0103,R0912,R0914,R0915

u"""
    dbxml2rst.hooks
    ~~~~~~~~~~~~~~~

    Hooks used by the dbxml2rst library

    :copyright:  Copyright (C) 2016  Markus Heiser
    :license:    GPL V3.0, see LICENSE for details.
"""

# ==============================================================================
# imports
# ==============================================================================

from fspath import FSPath
from .nodes import XMLTag, Table

# ==============================================================================
# constants
# ==============================================================================

RESOUCE_FORMAT = "%s_files"

# ==============================================================================
def hook_copy_file_resource(srcFolder):
# ==============================================================================

    srcFolder = FSPath(srcFolder)

    def hookFunc(node, rstPrefix, parseData):  # pylint: disable=W0613

        # run this hook only on the root node
        if node.getparent() is not None:
            return node

        # are there any filerefs in?
        filerefList = node.findall(".//*[@fileref]")
        if not filerefList:
            return node

        thisFile   = FSPath(parseData.fname)
        bookBase   = FSPath(parseData.folder)

        bookOffset = thisFile.DIRNAME
        resFolder  = FSPath(RESOUCE_FORMAT % thisFile.BASENAME.SKIPSUFFIX)
        dstFolder  = bookBase / bookOffset / resFolder

        dstFolder.makedirs()

        for tag in filerefList:
            fileref = FSPath(tag.get("fileref")).BASENAME
            src = next(srcFolder.reMatchFind(fileref), None)
            if src is None:
                raise Exception("fileref: %s could not found in %s" % (fileref, srcFolder))
            src.copyfile(dstFolder)
            tag.set("fileref", resFolder / fileref )
            #SDK.CONSOLE()
        return node
    return hookFunc


# ==============================================================================
def hook_chunk_by_tag(*chunkPathes):
# ==============================================================================

    u"""
    Chunk DocBook XML document into XML fragments.

    Requirement for the division is an ID (e.g. ``<chapter id="intro" ...``)
    """
    chunkPathes = chunkPathes

    def hookFunc(node, rstPrefix, parseData): # pylint: disable=W0613

        # run this hook only on the root node
        if node.getparent() is not None:
            return node
        realNode = node

        if (node.tag == "dummy"
            and len(node) == 1
            and node[0].get("chunkNode") is not None):
            realNode = node[0]

        for tag in chunkPathes:
            # pylint: disable=R0204
            chunkNodes = realNode.findall("%s" % tag)
            for elem in chunkNodes:
                if elem.get("chunkNode") is not None:
                    continue
                ID = elem.get("id")
                if ID is None:
                    # generate unique ID by counting preceding siblings on any
                    # hierarchy level.
                    _p = elem
                    ID = []
                    while _p is not None:
                        if _p.tag == "dummy":
                            break
                        ID.insert(0, len(list(_p.itersiblings(preceding=True))))
                        _p = _p.getparent()
                    ID = "-".join(["%03d" % x for x in ID])
                    ID = "%s-%s" % (parseData.fname.BASENAME.SKIPSUFFIX, ID)
                ext_entity = parseData.fname.DIRNAME / ("%s.xml" % ID)
                XMLTag.chunkNode(
                    elem
                    , parseData.folder
                    , ext_entity.suffix(parseData.fname.SUFFIX))
            if len(chunkNodes):
                break
        return node
    return hookFunc

# ==============================================================================
def hook_html2db_table(node, rstPrefix, parseData): # pylint: disable=W0613
# ==============================================================================
    u"""This hook converts a HTML table to a DocBook table

    This is done by simply change ``<tr>`` and ``<td>`` (``<th>``) tags to
    ``<row>`` and ``<entry>`` tags
    """
    # run this hook only on the root node
    if node.getparent() is not None:
        return node

    for elem in node.findall(".//tr"):
        newNode = XMLTag.copyNode(elem, "row", moveID=True)
        XMLTag.replaceNode(elem, newNode)

    for elem in node.findall(".//th") + node.findall(".//td"):
        newNode = XMLTag.copyNode(elem, "entry", moveID=True)
        XMLTag.replaceNode(elem, newNode)

    return node

# ==============================================================================
def hook_fix_broken_tables(fname_list=None, id_list=None):
# ==============================================================================

    u"""This hooks add missing colspecs to the *broken* table.

    A complete colspec definition is needed by pandoc, otherwise the build of
    the ASCII-art table fails within pandoc."""
    fname_list = fname_list or []
    id_list    = id_list    or []

    def hookFunc(node, rstPrefix, parseData):
        # pylint: disable=W0613, R0912

        if node.tag != "table":
            return node

        fname = parseData.folder.BASENAME / parseData.fname.SKIPSUFFIX
        if (node.get("id") not in id_list
            and fname not in fname_list):
            return node

        table  = node
        tgroup = table.find("tgroup")
        cols   = int(tgroup.get("cols"))
        thead  = tgroup.find("thead")
        tbody  = tgroup.find("tbody")

        if thead is not None:
            # is there any row in the header with more entries as defined cols?
            for row in thead.findall("row"):
                entries = row.findall("entry")
                if len(entries) > cols:
                    cols = len(entries)
                    tgroup.set("cols", str(cols))

        for row in tbody.findall("row"):
            # is there any row in the body with more entries as defined cols?
            entries = row.findall("entry")
            if len(entries) > cols:
                cols = len(entries)
                tgroup.set("cols", str(cols))

        if thead is not None:
            # add missing entries to header rows
            for row in thead.findall("row"):
                entries = row.findall("entry")
                if len(entries) < cols:
                    for _x in range(cols - len(entries)):
                        row.append(node.makeelement("entry"))

        # add missing entries to body rows
        for row in tbody.findall("row"):
            entries = row.findall("entry")

            if len(entries) < cols:
                for _x in range(cols - len(entries)):
                    row.append(node.makeelement("entry"))
        return node
    return hookFunc

# ==============================================================================
def hook_replaceTag(id2TagMap):
# ==============================================================================

    id2TagMap = id2TagMap

    def hookFunc(node, rstPrefix, parseData):  # pylint: disable=W0613
        # run this hook only on the root node
        if node.getparent() is not None:
            return node
        for ID, newTag in id2TagMap.items():
            elem = node.find(".//*[@id='%s']" % ID)
            if elem is not None:
                newNode = XMLTag.copyNode(elem, newTag, moveID=True)
                XMLTag.replaceNode(elem, newNode)
        return node
    return hookFunc


# ==============================================================================
def hook_drop_usless_informaltables(node, _rstPrefix, _parseData):
# ==============================================================================

    u"""Hook to convert useless informatables to (e.g) paragraphs"""
    # run this hook only on the root node
    if node.getparent() is not None:
        return node

    for table in node.findall(".//informaltable"):
        tbody = table.find(".//tbody")
        max_cols = 0
        for row in tbody.findall(".//row"):
            c = len(row.findall(".//entry"))
            if c > max_cols:
                max_cols = c
        section = node.makeelement("section")
        if max_cols < 2:
            for entry in tbody.find(".//entry"):
                para = XMLTag.copyNode(entry, "para", moveID=True)
                section.append(para)
            XMLTag.replaceNode(table, section)
    return node

# ==============================================================================
def hook_flatten_tables(table_id_list="all"):
# ==============================================================================

    u"""Hook to convert tables into a double-stage list.

    This hook converts a tables (by id or "all") into the ``flat-table``
    directive"""

    table_id_list = table_id_list

    def hookFunc(node, rstPrefix, parseData):   # pylint: disable=W0613
        # run this hook only on the root node
        if node.getparent() is not None:
            return node

        for table in node.findall(".//table") + node.findall(".//informaltable"):
            if (table_id_list == "all"
                or table.get("id") in table_id_list):

                # seek column widths and col-spans from DocBook is the hell,
                # particularly there are <entrytbl> which left up to the outer
                # table and broken colspec definitions which has not been
                # rejected by the docbook toolchains. These colspecs must be
                # *repaired* in any matter.

                colspec = {}
                colspecByNumber = {}

                for colspec_count, c in enumerate(table.findall(".//colspec")):
                    colnum = c.get("colnum")
                    if colnum is not None:
                        try:
                            colnum = int(colnum)
                        except Exception: # pylint: disable=W0703
                            pass
                    if colnum is None:
                        colnum = colspec_count
                    colname = c.get("colname")
                    if colname is None:
                        colname = ""
                    align = c.get("align")
                    colwidth = c.get("colwidth")
                    if colwidth is not None:
                        colwidth = colwidth.replace("*","")
                        # some colspec definition use the "&#x22C6;" entity
                        colwidth = colwidth.replace(u"⋆", "")
                        try:
                            colwidth = int(colwidth)
                        except Exception:  # pylint: disable=W0703
                            colwidth = None
                    colspec[colname] = (colnum, align, colwidth )
                    colspecByNumber[colnum] = (colname, align, colwidth)

                spanspec = {}
                for item in table.findall(".//spanspec"):
                    spanname = item.get("spanname")
                    namest   = item.get("namest")
                    nameend  = item.get("nameend")
                    if spanname is None or namest is None or nameend is None:
                        continue
                    start = colspec.get(namest, [None, None,None])[0]
                    end   = colspec.get(nameend, [None, None,None])[0]
                    if start is None or end is None:
                        continue
                    spanspec[spanname] = end - start


                # convert table to double-stage list

                max_cols = 0
                row_count = 0
                flatTable = node.makeelement("itemizedlist")

                # eat all rows, include the rows from entrytbl

                for row in table.findall(".//row"):
                    row_count += 1
                    flatRow = node.makeelement("listitem")
                    row_id = row.get("id")
                    if row_id:
                        flatRow.text = ".. _`%s`:" % row_id
                    else:
                        flatRow.text = ".. table row"
                        #flatRow.text = ".. row %s" % row_count
                    flatTable.append(flatRow)
                    colList = node.makeelement("itemizedlist")
                    flatRow.append(colList)
                    col_count = 0
                    for entry in row.findall(".//entry"):
                        col_count += 1
                        cspan = spanspec.get(entry.get("spanname"), 0)
                        if cspan == 0:
                            # the colspan attribut comes from tables which has
                            # been converted from html (see hook_html2db_table)
                            cspan = int(entry.get("colspan", 1)) - 1
                        newCol = node.makeelement("listitem")

                        # a ID in a cell needs some extras
                        cell_id = entry.get("id")
                        if cell_id is not None:
                            del entry.attrib["id"]
                            para_id= node.makeelement("para")
                            para_id.text = (".. _`%s`:\n\n" % cell_id)
                            newCol.append(para_id)

                        # move content of entry to a para and insert
                        # rat-spanning markup
                        para   = XMLTag.copyNode(entry, "para", moveID=False)
                        if cspan:
                            para.text = (":cspan:`%s` " % cspan) + (para.text or "")
                            col_count += cspan
                        morerows = entry.get("morerows", 0)
                        if morerows == 0:
                            # the rowspan attribut comes from tables which has
                            # been converted from html (see hook_html2db_table)
                            morerows = int(entry.get("rowspan", 1)) -1
                        if morerows:
                            para.text = (":rspan:`%s` " % morerows) + (para.text or "")
                        newCol.append(para)
                        colList.append(newCol)
                    if col_count > max_cols:
                        max_cols = col_count

                # estimate colwidths

                widths = []
                for i in range(max_cols):
                    colname, align, colwidth = colspecByNumber.get(i, (None, None, None))
                    if colwidth is None:
                        colwidth = 1
                    widths.append(str(colwidth))

                # use widths only when they are meaningful
                useWidth = False
                for w in widths:
                    if w != widths[0]:
                        useWidth = True
                        break
                if len(colspec) > max_cols:
                    # The colspec definition has more entries than columns
                    # existing in the table definition. This indicates, that the
                    # colspec definition is buggy. I don't use width definitions
                    # from buggy colspecs
                    useWidth = False

                # insert prefix

                ctx = Table().getContext(table)
                ctx.header_rows  = len(table.findall(".//thead/row") or [])
                ctx.stub_columns = 1 if table.get("rowheader") == "firstcol" else 0
                ctx.widths = " ".join(widths)

                preText = "\n" if not ctx.ID else Table.rstAnchor
                preText +=  "\n.. flat-table::%(title)s"
                preText += "\n    :header-rows:  %(header_rows)s"
                preText += "\n    :stub-columns: %(stub_columns)s"
                if useWidth:
                    preText += "\n    :widths:       %(widths)s"
                preText += "\n    "
                preText += "\n%(tableStartMark)s"
                new = XMLTag.getInjBlockTag()
                new.text += preText % ctx
                table.addprevious(new)

                # insert postfix

                rstPostText = "\n%(tableEndMark)s\n"
                new = XMLTag.getInjBlockTag()
                new.text += rstPostText % ctx
                table.addnext(new)

                # replace table

                XMLTag.replaceNode(table, flatTable)
        return node
    return hookFunc


