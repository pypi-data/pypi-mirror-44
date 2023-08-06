## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">
    $(function() {
        $('#profile-tabs').tabs();
    });
  </script>
</%def>

<div id="profile-tabs">
  <ul>
    <li><a href="#personal-tab">Personal</a></li>
    <li><a href="#customer-tab">Customer</a></li>
    <li><a href="#employee-tab">Employee</a></li>
  </ul>

  <div id="personal-tab">

    <div class="field-wrapper first_name">
      <div class="field-row">
        <label>First Name</label>
        <div class="field">
          ${person.first_name}
        </div>
      </div>
    </div>

    <div class="field-wrapper middle_name">
      <div class="field-row">
        <label>Middle Name</label>
        <div class="field">
          ${person.middle_name}
        </div>
      </div>
    </div>

    <div class="field-wrapper last_name">
      <div class="field-row">
        <label>Last Name</label>
        <div class="field">
          ${person.last_name}
        </div>
      </div>
    </div>

    <div class="field-wrapper street">
      <div class="field-row">
        <label>Street 1</label>
        <div class="field">
          ${person.address.street if person.address else ''}
        </div>
      </div>
    </div>

    <div class="field-wrapper street2">
      <div class="field-row">
        <label>Street 2</label>
        <div class="field">
          ${person.address.street2 if person.address else ''}
        </div>
      </div>
    </div>

    <div class="field-wrapper city">
      <div class="field-row">
        <label>City</label>
        <div class="field">
          ${person.address.city if person.address else ''}
        </div>
      </div>
    </div>

    <div class="field-wrapper state">
      <div class="field-row">
        <label>State</label>
        <div class="field">
          ${person.address.state if person.address else ''}
        </div>
      </div>
    </div>

    <div class="field-wrapper zipcode">
      <div class="field-row">
        <label>Zipcode</label>
        <div class="field">
          ${person.address.zipcode if person.address else ''}
        </div>
      </div>
    </div>

  </div><!-- personal-tab -->

  <div id="customer-tab">
    % for customer in person.customers:

        <div class="field-wrapper id">
          <div class="field-row">
            <label>ID</label>
            <div class="field">
              ${customer.id or ''}
            </div>
          </div>
        </div>

        <div class="field-wrapper name">
          <div class="field-row">
            <label>Name</label>
            <div class="field">
              ${customer.name}
            </div>
          </div>
        </div>

    % endfor
  </div><!-- customer-tab -->

  <div id="employee-tab">
    % if person.employee:

        <div class="field-wrapper id">
          <div class="field-row">
            <label>ID</label>
            <div class="field">
              ${person.employee.id or ''}
            </div>
          </div>
        </div>

        <div class="field-wrapper display_name">
          <div class="field-row">
            <label>Display Name</label>
            <div class="field">
              ${person.employee.display_name or ''}
            </div>
          </div>
        </div>

        <div class="field-wrapper status">
          <div class="field-row">
            <label>Status</label>
            <div class="field">
              ${enum.EMPLOYEE_STATUS[person.employee.status]}
            </div>
          </div>
        </div>

    % else:
        <p>${person} has never been an employee.</p>
    % endif
  </div><!-- employee-tab -->

</div><!-- profile-tabs -->
