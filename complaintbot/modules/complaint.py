from complaintbot import command, module, util, models


class ComplaintModule(module.Module):
    name = "Complaint"

    @command.desc("List the groups are you known to be a member of.")
    async def cmd_groups(self, msg):
        with models.Session() as session:
            groups = session.query(models.Group).filter_by(user_id=msg.from_id)
        lines = {}

        for grp in groups:
            lines[grp.tg_id] = f"**Identifier:** \n{grp.identifier}"

        sections = []
        for gid, identifier in lines.items():
            sections.append(
                f"**{gid}**:\n    \u2022 " + "\n    \u2022 ".join(ln) + "\n"
            )

        return "\n".join(sections)

    @command.desc("List all the complaints and their status so far.")
    async def cmd_list(self, msg):
        return f""

    @command.desc("Register a new complaint for a given group.")
    async def cmd_new(self, msg):
        return f""

    @command.desc("See details for a certain complaint.")
    async def cmd_see(self, msg):
        return f""

    @command.desc("Mark a complaint as resolved.")
    async def cmd_resolve(self, msg):
        return f""
