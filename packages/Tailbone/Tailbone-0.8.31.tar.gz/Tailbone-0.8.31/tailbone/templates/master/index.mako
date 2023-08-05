## -*- coding: utf-8; -*-
## ##############################################################################
## 
## Default master 'index' template.  Features a prominent data table and
## exposes a way to filter and sort the data, etc.  Some index pages also
## include a "tools" section, just above the grid on the right.
## 
## ##############################################################################
<%inherit file="/base.mako" />

<%def name="title()">${index_title}</%def>

<%def name="content_title()"></%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">
    $(function() {

        % if not use_buefy:
        $('.grid-wrapper').gridwrapper();
        % endif

        % if master.mergeable and request.has_perm('{}.merge'.format(permission_prefix)):

            $('form[name="merge-things"] button').button('option', 'disabled', $('.grid').gridcore('count_selected') != 2);

            $('.grid-wrapper').on('gridchecked', '.grid', function(event, count) {
                $('form[name="merge-things"] button').button('option', 'disabled', count != 2);
            });

            $('form[name="merge-things"]').submit(function() {
                var uuids = $('.grid').gridcore('selected_uuids');
                if (uuids.length != 2) {
                    return false;
                }
                $(this).find('[name="uuids"]').val(uuids.toString());
                $(this).find('button')
                    .button('option', 'label', "Preparing to Merge...")
                    .button('disable');
            });

        % endif

        % if master.bulk_deletable and request.has_perm('{}.bulk_delete'.format(permission_prefix)):

        $('form[name="bulk-delete"] button').click(function() {
            var count = $('.grid-wrapper').gridwrapper('results_count', true);
            if (count === null) {
                alert("There don't seem to be any results to delete!");
                return;
            }
            if (! confirm("You are about to delete " + count + " ${model_title_plural}.\n\nAre you sure?")) {
                return
            }
            $(this).button('disable').button('option', 'label', "Deleting Results...");
            $('form[name="bulk-delete"]').submit();
        });

        % endif

        % if master.supports_set_enabled_toggle and request.has_perm('{}.enable_disable_set'.format(permission_prefix)):
            $('form[name="enable-set"] button').click(function() {
                var form = $(this).parents('form');
                var uuids = $('.grid').gridcore('selected_uuids');
                if (! uuids.length) {
                    alert("You must first select one or more objects to enable.");
                    return false;
                }
                if (! confirm("Are you sure you wish to ENABLE the " + uuids.length + " selected objects?")) {
                    return false;
                }
                form.find('[name="uuids"]').val(uuids.toString());
                disable_button(this);
                form.submit();
            });

            $('form[name="disable-set"] button').click(function() {
                var form = $(this).parents('form');
                var uuids = $('.grid').gridcore('selected_uuids');
                if (! uuids.length) {
                    alert("You must first select one or more objects to disable.");
                    return false;
                }
                if (! confirm("Are you sure you wish to DISABLE the " + uuids.length + " selected objects?")) {
                    return false;
                }
                form.find('[name="uuids"]').val(uuids.toString());
                disable_button(this);
                form.submit();
            });
        % endif

        % if master.set_deletable and request.has_perm('{}.delete_set'.format(permission_prefix)):
            $('form[name="delete-set"] button').click(function() {
                var form = $(this).parents('form');
                var uuids = $('.grid').gridcore('selected_uuids');
                if (! uuids.length) {
                    alert("You must first select one or more objects to delete.");
                    return false;
                }
                if (! confirm("Are you sure you wish to DELETE the " + uuids.length + " selected objects?")) {
                    return false;
                }
                form.find('[name="uuids"]').val(uuids.toString());
                disable_button(this);
                form.submit();
            });
        % endif
    });
  </script>
</%def>

<%def name="context_menu_items()">
  % if master.results_downloadable_csv and request.has_perm('{}.results_csv'.format(permission_prefix)):
      <li>${h.link_to("Download results as CSV", url('{}.results_csv'.format(route_prefix)))}</li>
  % endif
  % if master.results_downloadable_xlsx and request.has_perm('{}.results_xlsx'.format(permission_prefix)):
      <li>${h.link_to("Download results as XLSX", url('{}.results_xlsx'.format(route_prefix)))}</li>
  % endif
  % if master.creatable and master.show_create_link and request.has_perm('{}.create'.format(permission_prefix)):
      % if master.creates_multiple:
          <li>${h.link_to("Create new {}".format(model_title_plural), url('{}.create'.format(route_prefix)))}</li>
      % else:
          <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
      % endif
  % endif
</%def>

<%def name="grid_tools()">

  ## merge 2 objects
  % if master.mergeable and request.has_perm('{}.merge'.format(permission_prefix)):
      ${h.form(url('{}.merge'.format(route_prefix)), name='merge-things')}
      ${h.csrf_token(request)}
      ${h.hidden('uuids')}
      <button type="submit">Merge 2 ${model_title_plural}</button>
      ${h.end_form()}
  % endif

  ## enable / disable selected objects
  % if master.supports_set_enabled_toggle and request.has_perm('{}.enable_disable_set'.format(permission_prefix)):
      ${h.form(url('{}.enable_set'.format(route_prefix)), name='enable-set')}
      ${h.csrf_token(request)}
      ${h.hidden('uuids')}
      <button type="button">Enable Selected</button>
      ${h.end_form()}

      ${h.form(url('{}.disable_set'.format(route_prefix)), name='disable-set')}
      ${h.csrf_token(request)}
      ${h.hidden('uuids')}
      <button type="button">Disable Selected</button>
      ${h.end_form()}
  % endif

  ## delete selected objects
  % if master.set_deletable and request.has_perm('{}.delete_set'.format(permission_prefix)):
      ${h.form(url('{}.delete_set'.format(route_prefix)), name='delete-set')}
      ${h.csrf_token(request)}
      ${h.hidden('uuids')}
      <button type="button">Delete Selected</button>
      ${h.end_form()}
  % endif

  ## delete search results
  % if master.bulk_deletable and request.has_perm('{}.bulk_delete'.format(permission_prefix)):
      ${h.form(url('{}.bulk_delete'.format(route_prefix)), name='bulk-delete')}
      ${h.csrf_token(request)}
      <button type="button">Delete Results</button>
      ${h.end_form()}
  % endif

</%def>


% if use_buefy:
    ${grid.render_buefy(grid_columns=grid_columns, grid_data=grid_data, static_data=static_data)|n}

% else:
    ## no buefy, so do the traditional thing
    ${grid.render_complete(tools=capture(self.grid_tools).strip(), context_menu=capture(self.context_menu_items).strip())|n}

% endif
