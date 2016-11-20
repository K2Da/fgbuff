% from operator import attrgetter
<% player = pool.players[player_id] %>
% rebase('base.tpl', title=player.name)
<div class="col-xs-12">
<p class="display-4">{{player.name}}</p>
    <dl class="row">
        <dt class="col-sm-2 text-xs-right">Country</dt>
        <dd class="col-sm-9">{{!player.flag_span}} {{player.country_name}}</dd>
    </dl>
</div>

<div class="col-xs-12 col-lg-4">
    <h5>Matchups</h5>
    <table class="table">
    % for vs in sorted(pool.vs.values(), key=attrgetter('sort_key')):
        % if vs.player_id == player_id:
            <tr>
                <td>
                    vs. {{!vs.opponent.flag_span}} {{!vs.opponent.link}}<br />
                    {{!vs.wl}}
                </td>
                <td class="text-xs-center" style="vertical-align: middle; font-size: 150%;"><a href="/vs/{{player.url}}/{{vs.opponent.url}}">{{vs.win}} - {{vs.lose}}</a></td>
            </tr>
        % end
    % end
    </table>
</div>

<div class="col-xs-12 col-lg-8">
    <h5>Tournaments</h5>
    <table class="table">
    % for p in sorted(pool.participants.values(), key=attrgetter('end_at_desc')):
        % if p.player_id != player_id:
            % continue
        % end
        <tr>
            <td class="text-xs-left"><a href="#{{p.tournament.challo_url}}">{{p.tournament.name}}</a><td>
            <td class="text-xs-right">{{p.rank_emoji}}</td>
            <td class="text-xs-right">{{p.rank_text}}</td>
            <td class="text-xs-right" nowrap>{{p.tournament.date_string}}</td>
        </tr>
    % end
    </table>

    <h5>Matches</h5>
    <% tournament, group = None, None %>
    <table class="table">
    % for m in sorted(pool.matches.values(), key=attrgetter('end_at_desc', 'tournament_id', 'group_id', 'sort_key', 'id_desc')):
        % if tournament is None or tournament != m.tournament:
            <% participant = m.player1 if m.player1.player.id == player.id else m.player2 %>
            <tr>
                <th colspan="2" id="{{m.tournament.challo_url}}">{{! m.tournament.link_or_name}}</th>
                <td colspan="1" class="text-xs-right" nowrap>{{participant.rank_emoji}} {{participant.rank_text}}</td>
                <td colspan="3" class="text-xs-right">{{m.tournament.date_string}}</td>
            </tr>
        % end
        % if group is None or group != m.group:
            <tr>
                <th colspan="6">{{m.group.name}}</th>
            </tr>
        % end
        <tr>
            <%
                score_class = 'table-success' if (
                    m.p1_win and m.player1.player.id == player.id
                 or m.p2_win and m.player2.player.id == player.id
                ) else 'table-danger'
                left, center, right = (
                    m.player1, m.scores_csv, m.player2
                ) if m.player1.player.id == player.id else (
                    m.player2, m.scores_csv[::-1], m.player1
                )
            %>
            <td class="text-xs-center">{{m.round_name}}</td>
            <td class="text-xs-right">{{!left.link_or_text}}</td>
            <td class="text-xs-center {{score_class}}">{{center}}</td>
            <td class="text-xs-left">{{!right.player.flag_span}} {{!right.link_or_text}}</td>
            <td class="text-xs-right">{{right.rank_emoji}}</td>
            <td class="text-xs-right">{{right.rank_text}}</td>
        </tr>
        <% tournament, group = m.tournament, m.group %>
    % end
    </table>
</div>
