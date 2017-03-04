% from operator import attrgetter
% tournament = pool.tournaments[tournament_id]
% rebase('base.tpl', title=tournament.name)
<div class="col-xs-12">
    <h4 class="display-4">{{tournament.name}}</h4>
    <dl class="row">
        <dt class="col-sm-2 text-xs-right">Location</dt>
        <dd class="col-sm-9">{{!tournament.flag_span}} {{tournament.country_name}}</dd>
        <dt class="col-sm-2 text-xs-right">Date</dt>
        <dd class="col-sm-9">{{tournament.date_string}}</dd>
        <dt class="col-sm-2 text-xs-right">Labels</dt>
        <dd class="col-sm-9">
            <span class="tag tag tag-primary">{{tournament.version.text}}</span>
            % for p in tournament.props:
                <span class="tag tag tag-info">{{p.text}}</span>
            % end
        </dd>
        <dt class="col-sm-2 text-xs-right">Bracket</dt>
        <dd class="col-sm-9">{{!tournament.tournament_link}}</dd>
    </dl>
</div>

<div class="col-xs-12 col-lg-4">
    <h5>Participants</h5>
    <table class="table">
    % for p in sorted(pool.participants.values(), key=lambda p: p.rank_for_sort):
        <tr>
            <td>
                % wl = p.wl
                {{!p.player.flag_span}} {{!p.link_or_text}} {{! wl[0]}}<br />
                <div style="word-break: break-all; max-width: 220px;">
                    {{! wl[1]}}
                </div>
            </td>
            <td style="vertical-align: middle; font-size: 150%; text-align: center;">{{p.rank_text}}</td>
        </tr>
    % end
    </table>
</div>

<div class="col-xs-12 col-lg-8">
    <h5>Matches</h5>
    <table class="table">
    <% group = None %>
    % for m in sorted(pool.matches.values(), key=attrgetter('tournament_id', 'group_id', 'sort_key', 'id')):
        % if group is None or group != m.group:
            <thead>
                <tr>
                    <td colspan="3"><strong>{{m.group.name}}</strong></td>
                    <td colspan="2">{{m.group.tournament_type}}</td>
                </tr>
            </thead>
            <tbody>
        % end
        <tr>
            <% p1 = '<b><u>{0}</u></b>' if m.p1_win else '{0}' %>
            <% p2 = '<b><u>{0}</u></b>' if m.p2_win else '{0}' %>
            <td class="text-xs-center">{{m.round_name if m.round_name != round else ''}}</td>
            <td class="text-xs-right">{{!p1.format(m.player1.link_or_text)}} {{!m.player1.player.flag_span}}</td>
            <td class="text-xs-center" nowrap>{{m.scores_csv}}</td>
            <td class="text-xs-left">{{!m.player2.player.flag_span}} {{!p2.format(m.player2.link_or_text)}}</td>
            <% round = m.round_name %>
        </tr>
        <% group = m.group %>
    % end
        </tbody>
    </table>
</div>
