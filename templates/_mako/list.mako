<%inherit file="base.mako"/>

<%!
title = 'Bottled GridFS Admin'
%>

## Start body.
<h2>Add Filef7</h2>
${self.create_form()}
<h2>Found Files</h2>
${self.filef7_table()}
${self.footer()}
## End body.

<%def name="create_form()">
<form action="/create" method="POST" enctype="multipart/form-data">
    <table>
        <tr>
            <td>Name:</td>
            <td><input type="text" name="filename" /></td>
        </tr>
        <tr>
            <td>FileUpload:</td>
            <td><input type="file" name="inputFile" /></td>
        </tr>

        <tr>
            <td>Image:</td>
            <td>
                <input type="file" name="image" />
            </td>
        </tr>
        <tr>
            <td>Comments:</td>
            <td><textarea rows="3" name="text"></textarea></td>
        </tr>
        <tr>
            <td>
                <input type="submit" value="Create New File" onclick="toggle('spinner');">
                <img src="/static/images/spinner.gif" id="spinner" style="display: inline-table;">
            </td>
        </tr>
    </table>
</form>
</%def>

<%def name="filef7_table()">
<table id="files">
    %for filef7 in files:
    <tr>
        <td class="thumb">
            %if filef7.grid_id is not None:
            <a href="/image/${filef7.id}">
                <img src="/thumb/${filef7.id}" alt="" title="${filef7.filename|h}">
            </a>
            %endif
        </td>
        <td class="name">
            ${filef7.name}
        </td>
        <td class="text">
            ${filef7.text}
        </td>
        <td class="uploadDate">
            ${filef7.uploadDate.strftime('%X %d %b %y')}
        </td>
    </tr>
    %endfor
</table>
</%def>

<%def name="footer()">
<div id="navigation">
    %if prev_page is not None:
    <a href="/list/${prev_page}">&lt; Prev</a>
    %endif
    %if next_page is not None:
    <a href="/list/${next_page}">Next &gt;</a>
    %endif
</div>
<div id="poweredby">
    <img src="/static/images/poweredby.png" alt="Powered by Bottle + MongoDB">
</div>
</%def>
