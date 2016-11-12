% from operator import attrgetter
<% player1 = pool.players[p1] %>
<% player2 = pool.players[p2] %>
% rebase('base.tpl', title='{0} vs. {1}'.format(player1.name, player2.name))
<p class="display-4">{{player1.name}} vs. {{player2.name}}</p>

<h5>Matches</h5>
    <% tournament, group = None, None %>
    <table class="table">
    % for m in sorted(pool.matches.values(), key=attrgetter('end_at_desc', 'group_id', 'sort_key', 'id_desc')):
        % if tournament is None or tournament != m.tournament:
            <tr>
                <th colspan="3">{{! m.tournament.link_or_name}}</th>
                <td colspan="1" class="text-xs-right">{{m.tournament.date_string}}</td>
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
                    m.p1_win and m.player1.player.id == player1.id
                 or m.p2_win and m.player2.player.id == player1.id
                ) else 'table-danger'
                left, center, right = (
                    m.player1.link_or_text, m.scores_csv, m.player2.link_or_text
                ) if m.player1.player.id == player1.id else (
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
