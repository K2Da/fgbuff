% from operator import attrgetter
<% player = pool.players[player_id] %>
% rebase('base.tpl', title=player.name)
<p class="display-4">{{player.name}}</p>

<div class="col-xs-12 col-lg-4">
    <h5>Matchups</h5>
    <table class="table">
    % for vs in sorted(pool.vs.values(), key=attrgetter('sort_key')):
        <tr>
            <td>vs. {{!vs.opponent.link}}</td>
            <td class="text-xs-center"><a href="/vs/{{player.url}}/{{vs.opponent.url}}">{{vs.win}} - {{vs.lose}}</a></td>
        </tr>
    % end
    </table>
</div>

<div class="col-xs-12 col-lg-8">
    <h5>Matches</h5>
    <% tournament, group = None, None %>
    <table class="table">
    % for m in sorted(pool.matches.values(), key=attrgetter('end_at_desc', 'group_id', 'sort_key', 'id_desc')):
        % if tournament is None or tournament != m.tournament:
            <% participant = m.player1 if m.player1.player.id == player.id else m.player2 %>
            <tr>
                <th colspan="2">{{! m.tournament.link_or_name}}</th>
                <td colspan="1" class="text-xs-right">Rank {{participant.final_rank}}</td>
                <td colspan="1" class="text-xs-right">{{m.tournament.end_at}}</td>
            </tr>
        % end
        % if group is None or group != m.group:
            <tr>
                <th colspan="4">{{m.group.name}}</th>
            </tr>
        % end
        <tr>
            <%
                score_class = 'table-success' if (
                    m.p1_win and m.player1.player.id == player.id
                 or m.p2_win and m.player2.player.id == player.id
                ) else 'table-danger'
                left, center, right = (
                    m.player1.link_or_text, m.scores_csv, m.player2.link_or_text
                ) if m.player1.player.id == player.id else (
                    m.player2.link_or_text, m.scores_csv[::-1], m.player1.link_or_text
                )
            %>
            <td class="text-xs-center">{{m.round_name}}</td>
            <td class="text-xs-right">{{!left}}</td>
            <td class="text-xs-center {{score_class}}">{{center}}</td>
            <td class="text-xs-left">{{!right}}</td>
        </tr>
        <% tournament, group = m.tournament, m.group %>
    % end
    </table>
</div>
