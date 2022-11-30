import logging
import sys, traceback
# setting up logger
log = logging.getLogger()
log.setLevel(logging.INFO)


def pin_filter(partner_ids, pin_code_inc_df, pin_code_exc_df, pin):
    try:
        filtered_patner_ids = []
        for partner_id in partner_ids:
            pin_code_inc_df['partnerid'] = pin_code_inc_df['partnerid'].astype(int)
            pin_code_exc_df['partnerid'] = pin_code_exc_df['partnerid'].astype(int)
            locations_inc = pin_code_inc_df[pin_code_inc_df['partnerid'] == int(partner_id)]['Pincode'].to_list()
            locations_inc = [str(i) for i in locations_inc]
            locations_exc = pin_code_exc_df[pin_code_exc_df['partnerid'] == int(partner_id)]['Pincode'].to_list()
            locations_exc = [str(i) for i in locations_exc]
            if len(locations_inc) != 0:
                if pin in locations_inc:
                    pass
                else:
                    if partner_id in partner_ids:
                        filtered_patner_ids.append(partner_id)
            else:
                pass
            if len(locations_exc) != 0:
                if pin in locations_exc:
                    if partner_id in partner_ids:
                        filtered_patner_ids.append(partner_id)
                else:
                    pass
            else:
                pass
        if len(filtered_patner_ids) > 0:
            partner_ids = [partner_id for partner_id in partner_ids if partner_id not in filtered_patner_ids]
        else:
            pass
        # partners = {"partner_ids" : partner_ids
            # ,
            #         "filtered_patner_ids" : filtered_patner_ids
            #         }
        return partner_ids
        # log.info('Filtering PINs')
    except Exception as e:
        log.error(e)
        tb = sys.exc_info()[-1]
        stk = traceback.extract_tb(tb, 1)
        fname = stk[0][2]
        log.info(fname)
        raise Exception(fname)