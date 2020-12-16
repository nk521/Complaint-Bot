from complaintbot import command, module, util, models


class ComplaintModule(module.Module):
    name = "Complaint"

    @command.desc("List all the complaints and their status so far.")
    async def cmd_list(self, msg):
        with models.session_scope() as session:
            u = session.query(models.User).filter_by(tg_id=msg.from_id)
            if u is None:
                u = models.User(tg_id=msg.from_id)
                session.add(u)
                session.commit()
            threads = session.query(models.Thread).filter_by(by_user_id=msg.from_id)
        lines = [f"**Thread:** \n{th.id}" for th in threads]
        if lines:
            return "\n".join(lines)
        return "You have no threads yet!"

    @command.desc("Register a new complaint for a given group.")
    async def cmd_new(self, msg):
        return f""

    @command.desc("See details for a certain complaint.")
    async def cmd_see(self, msg):
        return f""

    @command.desc("Mark a complaint as resolved.")
    async def cmd_resolve(self, msg):
        return f""
