## -*- coding: utf-8; -*-
<div class="newfilters">

  ${h.form(form.action_url, method='get')}
    ${h.hidden('reset-to-default-filters', value='false')}
    ${h.hidden('save-current-filters-as-defaults', value='false')}

    <fieldset>
      <legend>Filters</legend>
      % for filtr in form.iter_filters():
          <div class="filter" id="filter-${filtr.key}" data-key="${filtr.key}"${' style="display: none;"' if not filtr.active else ''|n}>
            ${h.checkbox('{}-active'.format(filtr.key), class_='active', id='filter-active-{}'.format(filtr.key), checked=filtr.active)}
            <label for="filter-active-${filtr.key}">${filtr.label}</label>
            <div class="inputs">
              ${form.filter_verb(filtr)}
              ${form.filter_value(filtr)}
            </div>
          </div>
      % endfor
    </fieldset>

    <div class="level">
      <div class="level-left">
        <div class="level-item">
          ## <button type="submit" class="button is-primary" id="apply-filters">Apply Filters</button>
          <a class="button is-primary">
            <span class="icon is-small">
              <i class="fas fa-check"></i>
            </span>
            <span>Apply Filters</span>
          </a>
        </div>
        <div class="level-item">
          <div class="select">
            <select id="add-filter">
              <option value="">Add Filter</option>
              % for filtr in form.iter_filters():
                  <option value="${filtr.key}"${' disabled="disabled"' if filtr.active else ''|n}>${filtr.label}</option>
              % endfor
            </select>
          </div>
        </div>
        <div class="level-item">
          ## <button type="button" class="button" id="default-filters">Default View</button>
          <a class="button">
            <span class="icon is-small">
              <i class="fas fa-home"></i>
            </span>
            <span>Default View</span>
          </a>
        </div>
        <div class="level-item">
          ## <button type="button" class="button" id="clear-filters">No Filters</button>
          <a class="button">
            <span class="icon is-small">
              <i class="fas fa-trash"></i>
            </span>
            <span>No Filters</span>
          </a>
        </div>
        % if allow_save_defaults and request.user:
            <div class="level-item">
              ## <button type="button" class="button" id="save-defaults">Save Defaults</button>
              <a class="button">
                <span class="icon is-small">
                  <i class="fas fa-save"></i>
                </span>
                <span>Save Defaults</span>
            </a>
            </div>
        % endif
      </div>
    </div>

  ${h.end_form()}
</div><!-- newfilters -->
